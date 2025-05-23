from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id', 'title', 'description', 'thumbnail_url', 
                  'published_at', 'channel_id', 'channel_title']