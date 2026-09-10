from django.contrib import admin
from .models import Category, Position

class PositionInline(admin.TabularInline):
    model = Position
    extra = 2
    fields = ('name_uz', 'name_oz', 'name_ru', 'name_en', 'order', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'icon', 'name_uz', 'name_oz', 'name_ru', 'name_en', 'positions_count', 'order', 'is_active', 'created_at')
    list_display_links = ('id', 'name_uz')
    list_filter = ('is_active',)
    search_fields = ('name_uz', 'name_oz', 'name_ru', 'name_en')
    list_editable = ('order', 'is_active')
    inlines = [PositionInline]

    def positions_count(self, obj):
        return obj.positions.count()
    positions_count.short_description = "Lavozimlar soni"

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'category', 'name_oz', 'name_ru', 'name_en', 'order', 'is_active', 'created_at')
    list_display_links = ('id', 'name_uz')
    list_filter = ('category', 'is_active')
    search_fields = ('name_uz', 'name_oz', 'name_ru', 'name_en', 'category__name_uz')
    list_editable = ('order', 'is_active')
