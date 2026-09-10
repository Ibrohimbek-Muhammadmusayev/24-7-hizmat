from django.contrib import admin
from .models import BotConfig

@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_running', 'call_center_phone', 'updated_at')
