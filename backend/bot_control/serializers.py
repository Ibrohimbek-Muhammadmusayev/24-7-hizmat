from rest_framework import serializers
from .models import BotConfig

class BotConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotConfig
        fields = [
            'id', 
            'token',
            'client_bot_token',
            'worker_bot_token',
            'is_running', 
            'pid', 
            'last_started_at',
            'monetization_enabled',
            'initial_free_credits',
            'job_posting_cost_credits',
            'credit_price_sum',
            'welcome_text', 
            'welcome_image_url', 
            'about_text', 
            'call_center_phone', 
            'help_text', 
            'app_url',
            'app_url_enabled',
            'updated_at'
        ]

class SendMessageSerializer(serializers.Serializer):
    chat_id = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
