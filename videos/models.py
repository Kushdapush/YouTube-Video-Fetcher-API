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
    
    def __str__(self):
        return self.title

class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    quota_exceeded = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key[:5]}...{self.key[-5:]} - {'Active' if self.is_active else 'Inactive'}"