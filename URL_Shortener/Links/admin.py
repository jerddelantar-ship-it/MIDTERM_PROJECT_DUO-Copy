from django.contrib import admin
from .models import URLMap, ClickStats

@admin.register(URLMap)
class URLMapAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'original_url', 'click_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['original_url', 'short_code', 'custom_alias']
    readonly_fields = ['click_count', 'last_accessed', 'created_at', 'updated_at']

@admin.register(ClickStats)
class ClickStatsAdmin(admin.ModelAdmin):
    list_display = ['link', 'clicked_at', 'ip_address']
    list_filter = ['clicked_at']
    readonly_fields = ['clicked_at']