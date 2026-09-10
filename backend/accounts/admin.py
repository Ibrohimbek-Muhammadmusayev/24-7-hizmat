from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'first_name', 'phone_number', 'role', 'language', 'region', 'category', 'position', 'is_online', 'is_busy')
    list_filter = ('role', 'language', 'region', 'category', 'is_online', 'is_busy', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'telegram_id')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Full-Xizmat Sozlamalari', {
            'fields': (
                'role', 'language', 'phone_number', 'telegram_id',
                'region', 'category', 'position', 'custom_category', 'custom_position',
                'is_online', 'is_busy', 'specialty', 'rating', 'job_credits'
            )
        }),
    )
