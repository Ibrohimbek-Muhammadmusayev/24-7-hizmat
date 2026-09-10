from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Order, JobPost, JobApplication
from .serializers import (
    OrderSerializer, CreateOrderSerializer, DispatchOrderSerializer, 
    UpdateOrderStatusSerializer, JobPostSerializer, JobApplicationSerializer, 
    OfferJobToWorkerSerializer
)
from accounts.models import User

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save()

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class DispatchOrderView(views.APIView):
    permission_classes = [permissions.AllowAny]
    """
    Call Center operator dispatches an order to a specific worker.
    """
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = DispatchOrderSerializer(data=request.data)
        if serializer.is_valid():
            worker_id = serializer.validated_data['worker_id']
            worker = get_object_or_404(User, pk=worker_id, role=User.Role.WORKER)
            
            order.assigned_worker = worker
            order.status = Order.Status.DISPATCHED
            order.save()

            worker.is_busy = True
            worker.save()

            # Realtime alert notification to worker via Django Channels
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"worker_alerts_{worker.id}",
                    {
                        "type": "new_job_alert",
                        "order": OrderSerializer(order).data
                    }
                )
            except Exception as e:
                print("WebSocket send error:", e)

            return Response({
                'status': 'success',
                'message': f'Buyurtma {worker.first_name} {worker.last_name}ga biriktirildi',
                'order': OrderSerializer(order).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateOrderStatusView(views.APIView):
    permission_classes = [permissions.AllowAny]
    """
    Worker or Call Center updates job status: STARTED -> FINISHED -> CANCELLED
    """
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = UpdateOrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            order.status = new_status
            if new_status == Order.Status.FINISHED:
                order.is_paid = True
            if new_status == Order.Status.FINISHED or new_status == Order.Status.CANCELLED:
                if order.assigned_worker:
                    order.assigned_worker.is_busy = False
                    order.assigned_worker.save()
            order.save()

            # Broadcast update to Live Map / Dashboard
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "live_map_group",
                    {
                        "type": "order_status_update",
                        "order": OrderSerializer(order).data
                    }
                )
            except Exception as e:
                print("WebSocket send error:", e)

            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkerJobHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(assigned_worker=user).order_by('-created_at')

from django.utils import timezone
from datetime import timedelta
from categories.models import Category
from locations.models import Region

class OrderStatsView(views.APIView):
    permission_classes = [permissions.AllowAny]
    """
    Kengaytirilgan biznes, marketing va hududiy analitika endpointi.
    """
    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)

        # 1. Orders KPI
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
        dispatched_orders = Order.objects.filter(status=Order.Status.DISPATCHED).count()
        started_orders = Order.objects.filter(status=Order.Status.STARTED).count()
        finished_orders = Order.objects.filter(status=Order.Status.FINISHED).count()
        cancelled_orders = Order.objects.filter(status=Order.Status.CANCELLED).count()

        total_revenue = Order.objects.filter(status=Order.Status.FINISHED).aggregate(Sum('price'))['price__sum'] or 0.0
        today_revenue = Order.objects.filter(status=Order.Status.FINISHED, updated_at__gte=today_start).aggregate(Sum('price'))['price__sum'] or 0.0

        avg_order_value = (total_revenue / finished_orders) if finished_orders > 0 else 0.0
        completion_rate = round((finished_orders / total_orders * 100), 1) if total_orders > 0 else 0.0
        cancellation_rate = round((cancelled_orders / total_orders * 100), 1) if total_orders > 0 else 0.0

        # 2. User & Audience Marketing Stats
        total_users = User.objects.count()
        total_bot_users = User.objects.filter(telegram_id__isnull=False).count()
        registered_users = User.objects.filter(is_registered=True).count()
        reg_conversion_rate = round((registered_users / total_users * 100), 1) if total_users > 0 else 0.0

        total_workers = User.objects.filter(role=User.Role.WORKER).count()
        active_workers = User.objects.filter(role=User.Role.WORKER, is_online=True).count()
        busy_workers = User.objects.filter(role=User.Role.WORKER, is_busy=True).count()
        worker_occupancy_rate = round((busy_workers / active_workers * 100), 1) if active_workers > 0 else 0.0

        total_clients = User.objects.filter(role=User.Role.CLIENT).count()
        both_bot_users = User.objects.filter(started_client_bot=True, started_worker_bot=True).count()

        # 3. Job Posts & Applications Stats
        total_job_posts = JobPost.objects.count()
        active_job_posts = JobPost.objects.filter(status=JobPost.Status.ACTIVE).count()
        completed_job_posts = JobPost.objects.filter(status=JobPost.Status.COMPLETED).count()
        cancelled_job_posts = JobPost.objects.filter(status=JobPost.Status.CANCELLED).count()

        daily_job_posts = JobPost.objects.filter(employment_type=JobPost.EmploymentType.DAILY).count()
        permanent_job_posts = JobPost.objects.filter(employment_type=JobPost.EmploymentType.PERMANENT).count()

        total_applications = JobApplication.objects.count()
        accepted_applications = JobApplication.objects.filter(status='accepted').count()
        pending_applications = JobApplication.objects.filter(status='pending').count()

        # 4. Regional Distribution (Viloyatlar kesimi)
        regions_data = []
        all_regions = Region.objects.all()
        for reg in all_regions:
            reg_users = User.objects.filter(region=reg).count()
            reg_workers = User.objects.filter(region=reg, role=User.Role.WORKER).count()
            reg_clients = User.objects.filter(region=reg, role=User.Role.CLIENT).count()
            reg_job_posts = JobPost.objects.filter(region=reg).count()
            
            if reg_users > 0 or reg_job_posts > 0:
                regions_data.append({
                    'id': reg.id,
                    'name': reg.name_uz,
                    'total_users': reg_users,
                    'workers': reg_workers,
                    'clients': reg_clients,
                    'job_posts': reg_job_posts,
                    'percentage': round((reg_users / total_users * 100), 1) if total_users > 0 else 0.0
                })
        
        # Sort regions by total users descending
        regions_data.sort(key=lambda x: x['total_users'], reverse=True)

        # 5. Language Breakdown (Tillar)
        languages_data = [
            {'code': 'uz', 'name': "O'zbekcha (Lotin)", 'count': User.objects.filter(language='uz').count()},
            {'code': 'oz', 'name': "Ўзбекча (Кирилл)", 'count': User.objects.filter(language='oz').count()},
            {'code': 'ru', 'name': "Русский", 'count': User.objects.filter(language='ru').count()},
            {'code': 'en', 'name': "English", 'count': User.objects.filter(language='en').count()},
        ]

        # 6. Demographics (Gender & Age Groups)
        gender_data = {
            'male': User.objects.filter(gender='male').count(),
            'female': User.objects.filter(gender='female').count(),
            'unknown': User.objects.filter(gender__isnull=True).count() + User.objects.filter(gender='').count()
        }

        age_groups = {
            '18_25': User.objects.filter(age__gte=18, age__lte=25).count(),
            '26_35': User.objects.filter(age__gte=26, age__lte=35).count(),
            '36_50': User.objects.filter(age__gte=36, age__lte=50).count(),
            '50_plus': User.objects.filter(age__gt=50).count(),
            'unspecified': User.objects.filter(age__isnull=True).count()
        }

        # 7. Growth Trends (Last 7 days daily dynamics)
        growth_days = []
        for i in range(6, -1, -1):
            day_dt = now - timedelta(days=i)
            day_start = day_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_dt.replace(hour=23, minute=59, end_second=59 if hasattr(day_dt, 'end_second') else 59, microsecond=999999) if False else (day_start + timedelta(days=1))
            
            day_label = day_start.strftime("%d-%b")
            day_users = User.objects.filter(date_joined__gte=day_start, date_joined__lt=day_end).count()
            day_jobs = JobPost.objects.filter(created_at__gte=day_start, created_at__lt=day_end).count()
            day_orders = Order.objects.filter(created_at__gte=day_start, created_at__lt=day_end).count()

            growth_days.append({
                'date': day_label,
                'new_users': day_users,
                'new_jobs': day_jobs,
                'new_orders': day_orders
            })

        # 8. Category distribution (Orders & Job Posts demand)
        category_distribution = []
        for cat in Category.objects.all():
            cat_orders = Order.objects.filter(category=cat).count()
            cat_jobs = JobPost.objects.filter(category=cat).count()
            cat_workers = User.objects.filter(category=cat, role=User.Role.WORKER).count()
            cat_revenue = Order.objects.filter(category=cat, status=Order.Status.FINISHED).aggregate(Sum('price'))['price__sum'] or 0.0
            
            percentage = round((cat_orders / total_orders * 100), 1) if total_orders > 0 else 0.0
            category_distribution.append({
                'id': cat.id,
                'name': cat.name,
                'icon': cat.icon,
                'order_count': cat_orders,
                'job_posts_count': cat_jobs,
                'workers_count': cat_workers,
                'revenue': float(cat_revenue),
                'percentage': percentage
            })
        category_distribution.sort(key=lambda x: (x['job_posts_count'] + x['order_count']), reverse=True)

        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'dispatched_orders': dispatched_orders,
            'started_orders': started_orders,
            'finished_orders': finished_orders,
            'cancelled_orders': cancelled_orders,
            'total_revenue': float(total_revenue),
            'today_revenue': float(today_revenue),
            'avg_order_value': float(avg_order_value),
            'completion_rate': completion_rate,
            'cancellation_rate': cancellation_rate,
            
            # Users & Marketing
            'total_users': total_users,
            'total_bot_users': total_bot_users,
            'registered_users': registered_users,
            'reg_conversion_rate': reg_conversion_rate,
            'total_workers': total_workers,
            'active_workers': active_workers,
            'busy_workers': busy_workers,
            'worker_occupancy_rate': worker_occupancy_rate,
            'total_clients': total_clients,
            'both_bot_users': both_bot_users,
            
            # Job Posts & Market
            'total_job_posts': total_job_posts,
            'active_job_posts': active_job_posts,
            'completed_job_posts': completed_job_posts,
            'cancelled_job_posts': cancelled_job_posts,
            'daily_job_posts': daily_job_posts,
            'permanent_job_posts': permanent_job_posts,
            'total_applications': total_applications,
            'accepted_applications': accepted_applications,
            'pending_applications': pending_applications,

            # Regional, Demographics & Trends
            'regions_data': regions_data,
            'languages_data': languages_data,
            'gender_data': gender_data,
            'age_groups': age_groups,
            'growth_days': growth_days,
            'category_distribution': category_distribution
        })


class JobPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = JobPostSerializer

    def get_queryset(self):
        qs = JobPost.objects.all().select_related('employer', 'category', 'position', 'region').prefetch_related('applications__worker').order_by('-created_at')
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        category_param = self.request.query_params.get('category')
        if category_param:
            qs = qs.filter(category_id=category_param)
        employment_type = self.request.query_params.get('employment_type')
        if employment_type:
            qs = qs.filter(employment_type=employment_type)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(description__icontains=search) |
                Q(custom_position_name__icontains=search) |
                Q(district__icontains=search) |
                Q(contact_name__icontains=search) |
                Q(contact_phone__icontains=search)
            )
        return qs

    def perform_create(self, serializer):
        # Agar admin yaratayotgan bo'lsa va employer ko'rsatilmagan bo'lsa
        employer = self.request.user if self.request.user.is_authenticated else User.objects.filter(role=User.Role.ADMIN).first()
        serializer.save(employer=employer)


class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = JobPostSerializer
    queryset = JobPost.objects.all().select_related('employer', 'category', 'position', 'region').prefetch_related('applications__worker')


class OfferJobToWorkerView(views.APIView):
    permission_classes = [permissions.AllowAny]
    """
    Admin or Call Center offers a specific JobPost directly to a worker via Telegram Bot.
    """
    def post(self, request, pk):
        job = get_object_or_404(JobPost, pk=pk)
        serializer = OfferJobToWorkerSerializer(data=request.data)
        if serializer.is_valid():
            worker_id = serializer.validated_data['worker_id']
            worker = get_object_or_404(User, pk=worker_id, role=User.Role.WORKER)

            # Send Telegram Bot message to worker if telegram_id exists
            if worker.telegram_id:
                try:
                    from bot_control.models import BotConfig
                    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
                    from django.conf import settings
                    import asyncio

                    config = BotConfig.get_config()
                    token = (config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')).strip()
                    if token:
                        bot_instance = Bot(token=token)
                        pos_title = job.position.name_uz if job.position else (job.custom_position_name or 'Ish')
                        price_display = job.price_amount if (not job.is_price_negotiable and job.price_amount) else "Kelishilgan"
                        
                        offer_text = (
                            f"🎯 <b>SIZGA MAXSUS ISH TAKLIFI YUBORILDI!</b>\n\n"
                            f"📢 <b>Lavozim:</b> {pos_title}\n"
                            f"🏢 <b>Soha:</b> {job.category.name_uz if job.category else 'Boshqa'}\n"
                            f"📍 <b>Manzil:</b> {job.region.name_uz if job.region else ''} {job.district or ''}\n"
                            f"💰 <b>Haq:</b> {price_display}\n"
                            f"📝 <b>Tavsif:</b> {job.description}\n\n"
                            f"<i>Ushbu ishni qabul qilish yoki batafsil ko'rish uchun quyidagi tugmani bosing:</i>"
                        )
                        keyboard = [
                            [
                                InlineKeyboardButton("💼 Ishni olish", callback_data=f"job_take_JP-{job.id}"),
                                InlineKeyboardButton("🔍 Faolligini tekshirish", callback_data=f"job_check_JP-{job.id}")
                            ]
                        ]
                        async_to_sync(bot_instance.send_message)(
                            chat_id=worker.telegram_id,
                            text=offer_text,
                            reply_markup=InlineKeyboardMarkup(keyboard),
                            parse_mode='HTML'
                        )
                except Exception as e:
                    print("Error sending offer to worker via bot:", e)

            return Response({
                'success': True,
                'message': f"Ish #{job.id} muvaffaqiyatli ravishda {worker.get_full_name() or worker.first_name} ga taklif qilindi!"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


