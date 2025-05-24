import requests
from datetime import datetime, timezone, timedelta
from django.conf import settings
from .models import APIKey
import logging
import time

logger = logging.getLogger(__name__)

def get_next_api_key():
    api_key = APIKey.objects.filter(is_active=True, quota_exceeded=False).order_by('last_used').first()
    if not api_key:
        logger.error("No active API keys available. Please add or activate API keys.")
        raise Exception("No active API keys available")
    
    # Update the last_used timestamp
    api_key.last_used = datetime.now(timezone.utc)
    api_key.save(update_fields=['last_used'])
    
    return api_key.key

def fetch_videos_from_youtube(search_query, published_after=None):
    try:
        api_key = get_next_api_key()
        if not published_after:
            # Default to searching videos published in the last day
            published_after = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': search_query,
            'type': 'video',
            'order': 'date',
            'publishedAfter': published_after,
            'key': api_key,
            'maxResults': 25
        }
        
        response = requests.get(url, params=params)
        
        # Handle API key quota exceeded error
        if response.status_code != 200:
            logger.error(f"YouTube API Error: Status {response.status_code}")
            logger.error(f"Response body: {response.text}")
            error_data = {}
            try:
                error_data = response.json()
                logger.error(f"Error details: {error_data}")
            except:
                pass

        if response.status_code == 403:
            error_reason = "Unknown error"
            try:
                error_data = response.json()
                if "error" in error_data and "errors" in error_data["error"]:
                    error_reason = error_data["error"]["errors"][0].get("reason", "Unknown")
                    logger.warning(f"Error reason: {error_reason}")
            except:
                pass
                
            # Check if it's specifically a quota exceeded error
            if "quotaExceeded" in response.text or error_reason == "quotaExceeded":
                logger.warning(f"API key quota exceeded for key: {api_key[-5:]}...")
                api_key_obj = APIKey.objects.get(key=api_key)
                api_key_obj.quota_exceeded = True
                api_key_obj.save()
                
                # Check if we have any more keys before recursing
                if APIKey.objects.filter(is_active=True, quota_exceeded=False).exists():
                    logger.info("Trying with another API key")
                    # Try again with a different key
                    return fetch_videos_from_youtube(search_query, published_after)
                else:
                    logger.critical("All API keys have exceeded their quota. Please add new API keys.")
                    return {"items": []}
            else:
                logger.error(f"API request denied for reason other than quota: {error_reason}")

        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        logger.error(f"Error fetching videos: {str(e)}")
        
        # If the error is about API keys, handle gracefully
        if "No active API keys available" in str(e):
            # Log a more helpful message for operators
            logger.critical(
                "YouTube API key issue: No active API keys available. "
                "Please add new API keys through the admin interface."
            )
            # Return empty results instead of failing completely
            return {"items": []}
            
        # For other errors, re-raise
        raise