from django.contrib import admin
from .models import Flavor, DailySelection


@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ['name', 'flavor_type', 'is_seasonal', 'status', 'created_at']
    list_filter = ['status', 'flavor_type', 'is_seasonal']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DailySelection)
class DailySelectionAdmin(admin.ModelAdmin):
    list_display = ['date', 'hit_of_the_day', 'updated_at']
    filter_horizontal = ['flavors']
    date_hierarchy = 'date'
