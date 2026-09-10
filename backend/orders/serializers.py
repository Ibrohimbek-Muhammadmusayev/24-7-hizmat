from rest_framework import serializers
from .models import Order, JobPost, JobApplication
from accounts.serializers import UserSerializer
from categories.serializers import CategorySerializer, PositionSerializer
from locations.serializers import RegionSerializer

class OrderSerializer(serializers.ModelSerializer):
    assigned_worker_detail = UserSerializer(source='assigned_worker', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'source', 'work_format', 'category', 'category_detail', 'title',
            'customer_name', 'customer_phone', 'customer_telegram_id',
            'address', 'latitude', 'longitude', 'service_type', 'description',
            'status', 'assigned_worker', 'assigned_worker_detail',
            'price', 'is_paid', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'source', 'work_format', 'category', 'title', 'customer_name', 'customer_phone',
            'customer_telegram_id', 'address', 'latitude', 'longitude',
            'service_type', 'description', 'price'
        ]

class DispatchOrderSerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()

class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)


class JobApplicationSerializer(serializers.ModelSerializer):
    worker_detail = UserSerializer(source='worker', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job_post', 'worker', 'worker_detail', 'proposal_message', 'status', 'applied_at']
        read_only_fields = ['id', 'applied_at']


class JobPostSerializer(serializers.ModelSerializer):
    employer_detail = UserSerializer(source='employer', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    position_detail = PositionSerializer(source='position', read_only=True)
    region_detail = RegionSerializer(source='region', read_only=True)
    applications = JobApplicationSerializer(many=True, read_only=True)

    class Meta:
        model = JobPost
        fields = [
            'id', 'employer', 'employer_detail', 'employment_type', 'category', 'category_detail',
            'position', 'position_detail', 'custom_position_name', 'description', 'photo_file_id',
            'workers_count', 'gender_requirement', 'start_time_type', 'custom_start_date',
            'is_price_negotiable', 'price_amount', 'region', 'region_detail', 'district', 'address',
            'latitude', 'longitude', 'contact_name', 'contact_phone', 'contact_telegram_username',
            'status', 'views_count', 'applications_count', 'applications', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'views_count', 'applications_count', 'created_at', 'updated_at']


class OfferJobToWorkerSerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()

