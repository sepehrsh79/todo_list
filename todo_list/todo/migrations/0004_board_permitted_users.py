# Generated by Django 5.1.3 on 2024-11-30 19:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_task_deadline'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='permitted_users',
            field=models.ManyToManyField(blank=True, related_name='permitted_boards', to=settings.AUTH_USER_MODEL),
        ),
    ]
