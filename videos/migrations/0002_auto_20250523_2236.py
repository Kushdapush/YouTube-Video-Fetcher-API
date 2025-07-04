# Generated by Django 5.2.1 on 2025-05-23 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        # Use Django's AddIndex operation instead of raw SQL
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['-published_at'], name='video_published_desc_idx'),
        ),
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['title'], name='video_title_idx'),
        ),
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['channel_title'], name='video_channel_title_idx'),
        ),
    ]
