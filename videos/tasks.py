from celery import shared_task
from datetime import datetime, timezone, timedelta
from .models import Video
from .utils import fetch_videos_from_youtube
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_latest_videos(search_query="cricket"):
    """
    Task to fetch the latest videos from YouTube API
    """
    try:
        # Get the timestamp of the most recent video
        latest_video = Video.objects.order_by('-published_at').first()
        published_after = None
        
        if latest_video:
            # Add a small buffer to avoid missing videos
            published_after = (latest_video.published_at - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Fetch videos from YouTube
        youtube_data = fetch_videos_from_youtube(search_query, published_after)
        
        # Process and save videos
        for item in youtube_data.get('items', []):
            video_id = item['id']['videoId']
            snippet = item['snippet']
            published_at = datetime.strptime(
                snippet['publishedAt'], 
                '%Y-%m-%dT%H:%M:%SZ'
            ).replace(tzinfo=timezone.utc)
            
            Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'published_at': published_at,
                    'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    'channel_title': snippet.get('channelTitle', ''),
                }
            )
        
        logger.info(f"Successfully fetched {len(youtube_data.get('items', []))} videos")
        return f"Fetched {len(youtube_data.get('items', []))} videos"
    
    except Exception as e:
        logger.error(f"Error fetching videos: {str(e)}")
        raise