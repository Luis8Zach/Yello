# Generated by Django 4.2.5 on 2023-12-08 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='post_videos/', verbose_name='Video'),
        ),
    ]
