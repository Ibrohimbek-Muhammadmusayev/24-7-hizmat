from rest_framework import views, status, permissions, generics, exceptions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import models
from .models import User, UserFeedback, WorkerPortfolio, WorkerReview
from .serializers import (
    UserSerializer, 
    LoginSerializer, 
    ToggleOnlineSerializer, 
    UpdateFCMTokenSerializer, 
    RegisterWorkerSerializer,
    UserFeedbackSerializer,
    WorkerPortfolioSerializer,
    WorkerReviewSerializer
)
from locations.models import WorkerLocation

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({'error': 'Login yoki parol noto\'g\'ri'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeAdminCredentialsView(views.APIView):
    """
    Dashboard settings: Allows logged in user (or admin) to update their username and password.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        current_username = request.data.get('current_username')
        new_username = request.data.get('new_username')
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        user = None
        if user_id:
            user = User.objects.filter(id=user_id).first()
        elif current_username:
            user = User.objects.filter(username=current_username).first()
        elif request.user.is_authenticated:
            user = request.user

        if not user:
            return Response({'error': "Foydalanuvchi hisobi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        # Agar joriy parol tekshirishi so'ralgan bo'lsa
        if current_password:
            if not user.check_password(current_password):
                return Response({'error': "Joriy (eski) parol noto'g'ri kiritildi!"}, status=status.HTTP_400_BAD_REQUEST)

        # Yangi login tekshiruvi
        if new_username and new_username.strip() and new_username.strip() != user.username:
            clean_username = new_username.strip()
            if User.objects.filter(username=clean_username).exclude(id=user.id).exists():
                return Response({'error': f"'{clean_username}' nomli login allaqachon mavjud! Boshqa login tanlang."}, status=status.HTTP_400_BAD_REQUEST)
            user.username = clean_username

        # Yangi parol tekshiruvi
        if new_password:
            if confirm_password and new_password != confirm_password:
                return Response({'error': "Yangi parollar bir-biriga mos kelmadi!"}, status=status.HTTP_400_BAD_REQUEST)
            if len(new_password) < 4:
                return Response({'error': "Parol kamida 4 ta belgidan iborat bo'lishi kerak!"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)

        user.save()

        # Generate new JWT tokens so the session stays updated
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': "Hisob ma'lumotlari (login va parol) muvaffaqiyatli o'zgartirildi!",
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

from django.http import FileResponse, Http404
from django.conf import settings
from datetime import datetime
import os
import shutil
import tempfile

class DownloadDatabaseBackupView(views.APIView):
    """
    Admin only: Downloads a live copy/backup of the SQLite database.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        db_path = settings.DATABASES['default']['NAME']
        if not os.path.exists(db_path):
            raise Http404("Ma'lumotlar bazasi fayli topilmadi!")

        # Create a safe snapshot copy so active DB connections aren't locked
        temp_dir = tempfile.gettempdir()
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"db_backup_24_7_ishlar_{date_str}.sqlite3"
        temp_backup_path = os.path.join(temp_dir, backup_filename)

        shutil.copy2(db_path, temp_backup_path)

        response = FileResponse(open(temp_backup_path, 'rb'), as_attachment=True, filename=backup_filename)
        return response

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ToggleOnlineView(views.APIView):
    def post(self, request):
        serializer = ToggleOnlineSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.is_online = serializer.validated_data['is_online']
            user.save()
            return Response({'status': 'success', 'is_online': user.is_online})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateFCMTokenView(views.APIView):
    def post(self, request):
        serializer = UpdateFCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.fcm_token = serializer.validated_data['fcm_token']
            user.save()
            return Response({'status': 'success'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkerListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(role=User.Role.WORKER).prefetch_related(
            'selected_positions', 'portfolio_items', 'received_reviews'
        ).select_related('region', 'category', 'position').order_by('-id')
        
        category_id = self.request.query_params.get('category_id')
        region_id = self.request.query_params.get('region_id')
        district = self.request.query_params.get('district')
        search = self.request.query_params.get('search')
        
        if category_id:
            queryset = queryset.filter(models.Q(category_id=category_id) | models.Q(selected_positions__category_id=category_id)).distinct()
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        if district:
            queryset = queryset.filter(district__icontains=district)
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(username__icontains=search) |
                models.Q(phone_number__icontains=search) |
                models.Q(specialty__icontains=search)
            )
        return queryset

class WorkerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.filter(role=User.Role.WORKER)

    def perform_destroy(self, instance):
        if instance.is_superuser or instance.is_staff or instance.role == User.Role.ADMIN:
            raise exceptions.ValidationError({'error': "Super admin yoki Admin hisobini o'chirib bo'lmaydi! Faqat tahrirlash mumkin."})
        super().perform_destroy(instance)

class RegisterWorkerView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterWorkerSerializer

    def perform_create(self, serializer):
        worker = serializer.save()
        # Initialize default location for new worker
        WorkerLocation.objects.get_or_create(
            worker=worker,
            defaults={'latitude': 41.311081, 'longitude': 69.240562, 'heading': 0.0}
        )

class UserListView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().prefetch_related('selected_positions').select_related('region', 'category', 'position').order_by('-id')
        role = self.request.query_params.get('role', None)
        search = self.request.query_params.get('search', None)
        has_telegram = self.request.query_params.get('has_telegram', None)
        bot_filter = self.request.query_params.get('bot_filter', None) # 'CLIENT', 'WORKER', 'BOTH'

        if role:
            queryset = queryset.filter(role=role)
        if has_telegram == 'true':
            queryset = queryset.filter(telegram_id__isnull=False)
        if bot_filter == 'CLIENT':
            queryset = queryset.filter(started_client_bot=True)
        elif bot_filter == 'WORKER':
            queryset = queryset.filter(started_worker_bot=True)
        elif bot_filter == 'BOTH':
            queryset = queryset.filter(started_client_bot=True, started_worker_bot=True)

        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(username__icontains=search) |
                models.Q(phone_number__icontains=search) |
                models.Q(telegram_id__icontains=search) |
                models.Q(specialty__icontains=search)
            )
        return queryset

    def perform_create(self, serializer):
        user = serializer.save()
        if not user.username:
            user.username = f"user_{user.id}"
            user.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('selected_positions').select_related('region', 'category', 'position')

    def perform_destroy(self, instance):
        if instance.is_superuser or instance.is_staff or instance.role == User.Role.ADMIN:
            raise exceptions.ValidationError({'error': "Super admin yoki Admin hisobini o'chirib bo'lmaydi! Faqat tahrirlash mumkin."})
        super().perform_destroy(instance)

class UpdateUserCreditsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        credits = request.data.get('job_credits', None)
        delta = request.data.get('add_credits', None)

        if credits is not None:
            try:
                user.job_credits = max(0, int(credits))
            except ValueError:
                return Response({'error': 'Kredit soni butun son bo\'lishi kerak'}, status=status.HTTP_400_BAD_REQUEST)
        elif delta is not None:
            try:
                user.job_credits = max(0, user.job_credits + int(delta))
            except ValueError:
                return Response({'error': 'Kredit miqdori butun son bo\'lishi kerak'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'job_credits yoki add_credits parametri kiritilmadi'}, status=status.HTTP_400_BAD_REQUEST)

        user.save()
        return Response({
            'message': f'{user.first_name or user.username} uchun kreditlar yangilandi: {user.job_credits} ta',
            'user': UserSerializer(user).data
        })

class UserFeedbackListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserFeedbackSerializer

    def get_queryset(self):
        queryset = UserFeedback.objects.select_related('user').all().order_by('-created_at')
        reviewed = self.request.query_params.get('is_reviewed')
        if reviewed is not None:
            queryset = queryset.filter(is_reviewed=(reviewed.lower() == 'true'))
        return queryset

class UserFeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserFeedbackSerializer
    queryset = UserFeedback.objects.all()

class RequestProfileUpdateView(views.APIView):
    """
    Admin paneldan foydalanuvchining ma'lumotlarini qayta to'ldirishga yuborish (needs_profile_update)
    va Telegram orqali bildirishnoma xabarini yuborish.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        reason = request.data.get('reason', '').strip()
        fields_list = request.data.get('fields', [])  # list of field keys: ['name', 'phone', 'location', 'positions', 'gender', 'age', 'work_schedule']
        if isinstance(fields_list, list) and fields_list:
            fields_str = ",".join(fields_list)
        else:
            fields_str = 'all'

        user.needs_profile_update = True
        user.profile_update_reason = reason
        user.profile_update_fields = fields_str
        user.is_registered = False  # Reset registration state so bot prompts for missing/targeted info
        user.save(update_fields=['needs_profile_update', 'profile_update_reason', 'profile_update_fields', 'is_registered'])

        # Translate field names for friendly notification
        field_labels_map = {
            'name': "Ism va Familiya",
            'phone': "Telefon raqam",
            'location': "Yashash manzili / GPS joylashuv",
            'positions': "Soha va mutaxassisliklar",
            'gender': "Jinsi",
            'age': "Yoshi",
            'work_schedule': "Bandlik turi va ish rejimi"
        }
        if fields_str != 'all':
            fields_human = ", ".join([field_labels_map.get(f, f) for f in fields_list])
            fields_instruction = f"📌 <b>Qayta kiritilishi kerak bo'lgan ma'lumotlar:</b> <b>{fields_human}</b>"
        else:
            fields_instruction = "📌 <b>Barcha shaxsiy ma'lumotlarni qaytadan to'ldirish talab etiladi.</b>"

        # Send Telegram notification if user has telegram_id
        if user.telegram_id:
            try:
                from bot_control.models import BotConfig
                from telegram import Bot
                from django.conf import settings
                from asgiref.sync import async_to_sync

                config = BotConfig.get_config()
                # Determine appropriate token
                token = (config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()
                if user.role == User.Role.CLIENT or user.started_client_bot:
                    token = (config.client_bot_token or token).strip()

                if token:
                    bot_instance = Bot(token=token)
                    reason_block = f"\n📝 <b>Sabab / Izoh:</b> <i>{reason}</i>\n" if reason else ""
                    notice_text = (
                        f"⚠️ <b>DIQQAT: Profil ma'lumotlaringizni yangilash talab qilinadi!</b>\n\n"
                        f"Hurmatli <b>{user.get_full_name() or user.first_name}</b>, administrator tomonidan profilingizdagi quyidagi ma'lumotlarni qayta kiritish so'ralmoqda:\n\n"
                        f"{fields_instruction}"
                        f"{reason_block}\n"
                        f"Iltimos, ma'lumotlarni to'g'rilash va faollashtirish uchun <b>/start</b> buyrug'ini yuboring."
                    )
                    async_to_sync(bot_instance.send_message)(
                        chat_id=user.telegram_id,
                        text=notice_text,
                        parse_mode='HTML'
                    )
            except Exception as e:
                print("Error notifying user via telegram on profile update request:", e)

        return Response({
            'success': True,
            'message': f"{user.get_full_name() or user.first_name} uchun ma'lumotlarni qayta to'ldirish holati faollashtirildi!",
            'user': UserSerializer(user).data
        })



