from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'customer_name', 'customer_phone', 'category', 'status', 'source', 'work_format', 'assigned_worker', 'price', 'is_paid', 'created_at')
    list_filter = ('status', 'source', 'work_format', 'category', 'is_paid')
    search_fields = ('customer_name', 'customer_phone', 'title', 'description', 'address')
    list_editable = ('status', 'is_paid')
