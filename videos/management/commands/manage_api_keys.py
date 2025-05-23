from django.core.management.base import BaseCommand, CommandError
import os
from dotenv import load_dotenv
from videos.models import APIKey

class Command(BaseCommand):
    help = 'Manage YouTube API keys - check status, load from .env, reset quotas'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, choices=['check', 'load', 'reset', 'add', 'flush'],
                           help='Action to perform: check, load, reset, add, flush')
        parser.add_argument('--key', type=str, help='API key to add (only for "add" action)')

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'check':
            self._check_keys()
        elif action == 'load':
            self._load_keys()
        elif action == 'reset':
            self._reset_keys()
        elif action == 'add':
            if not options['key']:
                raise CommandError('Please provide an API key with --key')
            self._add_key(options['key'])
        elif action == 'flush':
            self._flush_keys()

    def _check_keys(self):
        """Check the status of API keys"""
        self.stdout.write("API Key Status:")
        self.stdout.write("-" * 40)
        
        # Count keys
        total_keys = APIKey.objects.count()
        active_keys = APIKey.objects.filter(is_active=True).count()
        active_not_exceeded = APIKey.objects.filter(is_active=True, quota_exceeded=False).count()
        
        self.stdout.write(f"Total keys: {total_keys}")
        self.stdout.write(f"Active keys: {active_keys}")
        self.stdout.write(f"Active keys with quota not exceeded: {active_not_exceeded}")
        
        # Show key details
        self.stdout.write("\nKey details:")
        for key in APIKey.objects.all():
            self.stdout.write(
                f"- Key: {key.key[:5]}...{key.key[-5:]} | "
                f"Active: {key.is_active} | "
                f"Quota exceeded: {key.quota_exceeded} | "
                f"Last used: {key.last_used}"
            )

    def _load_keys(self):
        """Load API keys from .env file"""
        load_dotenv()
        
        # Get keys from environment
        api_keys = os.getenv('YOUTUBE_API_KEYS', '').split(',')
        loaded = 0
        
        for key in api_keys:
            key = key.strip()
            if not key:
                continue
                
            obj, created = APIKey.objects.update_or_create(
                key=key,
                defaults={'is_active': True, 'quota_exceeded': False}
            )
            
            if created:
                self.stdout.write(f"Added new key: {key[:5]}...{key[-5:]}")
            else:
                self.stdout.write(f"Updated existing key: {key[:5]}...{key[-5:]}")
            
            loaded += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {loaded} API keys'))

    def _reset_keys(self):
        """Reset quota_exceeded flag on all keys"""
        count = APIKey.objects.filter(is_active=True).update(quota_exceeded=False)
        self.stdout.write(self.style.SUCCESS(f'Reset quota exceeded flag for {count} API keys'))

    def _add_key(self, api_key):
        """Add a single API key"""
        obj, created = APIKey.objects.update_or_create(
            key=api_key,
            defaults={'is_active': True, 'quota_exceeded': False}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Added new API key: {api_key[:5]}...{api_key[-5:]}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated existing API key: {api_key[:5]}...{api_key[-5:]}'))

    def _flush_keys(self):
        """Delete all API keys"""
        count = APIKey.objects.all().count()
        APIKey.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} API keys'))