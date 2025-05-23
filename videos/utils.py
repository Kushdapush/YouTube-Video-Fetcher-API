import requests
from datetime import datetime, timezone
from django.conf import settings
from .models import APIKey

def get_next_api_key():
    api_key = APIKey.objects.filter(is_active=True, quota_exceeded=False).order_by('last_used').first()
    if not api_key:
        raise Exception("No active API keys available")
    return api_key.key

def fetch_videos_from_youtube(search_query, published_after=None):
    api_key = get_next_api_key()
    if not published_after:
        # Default to searching videos published in the last day
        published_after = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': search_query,
        'type': 'video',
        'order': 'date',
        'publishedAfter': published_after,
        'key': api_key,
        'maxResults': 50  # Maximum allowed by YouTube API
    }
    
    response = requests.get(url, params=params)
    
    # Handle API key quota exceeded error
    if response.status_code == 403:
        api_key_obj = APIKey.objects.get(key=api_key)
        api_key_obj.quota_exceeded = True
        api_key_obj.save()
        # Try again with a different key
        return fetch_videos_from_youtube(search_query, published_after)
    
    response.raise_for_status()
    return response.json()