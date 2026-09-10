from rest_framework import serializers
from .models import Category, Position

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'category', 'name_uz', 'name_oz', 'name_ru', 'name_en', 'order', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_oz', 'name_ru', 'name_en', 'icon', 'order', 'is_active', 'positions', 'created_at']

