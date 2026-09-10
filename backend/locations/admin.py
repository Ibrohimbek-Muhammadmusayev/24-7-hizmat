from django.contrib import admin
from .models import Region, WorkerLocation

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_oz', 'name_ru', 'name_en', 'order', 'is_active')
    list_display_links = ('id', 'name_uz')
    list_editable = ('order', 'is_active')
    search_fields = ('name_uz', 'name_oz', 'name_ru', 'name_en')
    list_filter = ('is_active',)

@admin.register(WorkerLocation)
class WorkerLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'latitude', 'longitude', 'heading', 'updated_at')
    search_fields = ('worker__first_name', 'worker__username', 'worker__phone_number')
