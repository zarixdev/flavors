# Django admin registrations kept as backup/fallback
# django.contrib.admin is currently disabled in INSTALLED_APPS
# Custom admin panel is available at /panel/

from django.contrib import admin
from django.utils.html import format_html
from .models import Flavor, DailySelection


@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ['photo_thumbnail', 'name', 'flavor_type', 'is_seasonal', 'status', 'created_at']
    list_filter = ['status', 'flavor_type', 'is_seasonal']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 50px; max-width: 100px;" /></a>',
                obj.photo.url, obj.photo.url
            )
        return "Brak zdjęcia"
    photo_thumbnail.short_description = "Zdjęcie"


@admin.register(DailySelection)
class DailySelectionAdmin(admin.ModelAdmin):
    list_display = ['date', 'hit_of_the_day', 'updated_at']
    filter_horizontal = ['flavors']
    date_hierarchy = 'date'
