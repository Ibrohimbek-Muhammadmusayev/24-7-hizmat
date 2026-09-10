from rest_framework import serializers
from .models import Region, WorkerLocation
from accounts.serializers import UserSerializer

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name_uz', 'name_oz', 'name_ru', 'name_en', 'order', 'is_active']

class WorkerLocationSerializer(serializers.ModelSerializer):
    worker_detail = UserSerializer(source='worker', read_only=True)

    class Meta:
        model = WorkerLocation
        fields = ['id', 'worker', 'worker_detail', 'latitude', 'longitude', 'heading', 'updated_at']

