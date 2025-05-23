from django.contrib import admin
from .models import Video, APIKey

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'channel_title', 'published_at')
    search_fields = ('title', 'description', 'channel_title')
    list_filter = ('published_at',)

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key_display', 'is_active', 'quota_exceeded', 'last_used')
    list_filter = ('is_active', 'quota_exceeded')
    
    def key_display(self, obj):
        return f"{obj.key[:5]}...{obj.key[-5:]}"
    key_display.short_description = 'API Key'