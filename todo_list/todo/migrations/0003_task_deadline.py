# Generated by Django 5.1.3 on 2024-11-30 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
