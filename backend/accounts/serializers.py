from rest_framework import serializers
from .models import User, WorkerPortfolio, WorkerReview, UserFeedback
from categories.serializers import CategorySerializer, PositionSerializer

class WorkerPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerPortfolio
        fields = ['id', 'file_id', 'caption', 'created_at']

class WorkerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerReview
        fields = ['id', 'client_name', 'client_phone', 'rating', 'comment', 'created_at']

class UserFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_phone = serializers.SerializerMethodField()
    user_telegram_id = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = UserFeedback
        fields = ['id', 'user', 'user_name', 'user_phone', 'user_telegram_id', 'user_role', 'message', 'is_reviewed', 'created_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name or obj.user.username} {obj.user.last_name or ''}".strip()

    def get_user_phone(self, obj):
        return obj.user.phone_number

    def get_user_telegram_id(self, obj):
        return obj.user.telegram_id

    def get_user_role(self, obj):
        return obj.user.role

class UserSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    position_details = PositionSerializer(source='position', read_only=True)
    selected_positions_details = PositionSerializer(source='selected_positions', many=True, read_only=True)
    portfolio_items = WorkerPortfolioSerializer(many=True, read_only=True)
    received_reviews = WorkerReviewSerializer(many=True, read_only=True)
    region_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'phone_number', 
            'role', 'language', 'telegram_id', 'gender', 'age',
            'region', 'region_name', 'district', 'street_address', 
            'latitude', 'longitude', 'address_title',
            'category', 'category_details', 'position', 'position_details',
            'selected_positions', 'selected_positions_details',
            'custom_category', 'custom_position',
            'employment_type', 'work_schedule',
            'is_online', 'is_busy', 'is_registered', 'notification_setting',
            'specialty', 'rating', 'completed_jobs_count', 'fcm_token', 'job_credits', 
            'started_client_bot', 'started_worker_bot',
            'portfolio_items', 'received_reviews', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_region_name(self, obj):
        return obj.region.name if obj.region else None

class RegisterWorkerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'phone_number', 'specialty', 'gender', 'age', 'district']

    def create(self, validated_data):
        validated_data['role'] = User.Role.WORKER
        validated_data['is_online'] = True
        validated_data['is_registered'] = True
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ToggleOnlineSerializer(serializers.Serializer):
    is_online = serializers.BooleanField()

class UpdateFCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()

