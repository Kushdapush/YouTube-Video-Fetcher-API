import os
from django.core.management.base import BaseCommand
from videos.models import APIKey

class Command(BaseCommand):
    help = 'Load YouTube API keys from environment variables'

    def handle(self, *args, **options):
        api_keys = os.getenv('YOUTUBE_API_KEYS', '').split(',')
        count = 0
        
        for key in api_keys:
            key = key.strip()
            if key:
                APIKey.objects.get_or_create(key=key)
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} API keys'))