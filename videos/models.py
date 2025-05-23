from django.db import models

# Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    published_at = models.DateTimeField()
    channel_id = models.CharField(max_length=100)
    channel_title = models.CharField(max_length=255)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            # Composite index for ordering and filtering
            models.Index(fields=['-published_at'], name='video_published_desc_idx'),
            # For search functionality
            models.Index(fields=['title'], name='video_title_idx'),
            models.Index(fields=['channel_title'], name='video_channel_title_idx'),
        ]
    
    def __str__(self):
        return self.title

class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    quota_exceeded = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key[:5]}...{self.key[-5:]} - {'Active' if self.is_active else 'Inactive'}"