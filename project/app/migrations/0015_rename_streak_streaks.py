# Generated by Django 4.2.7 on 2023-11-23 20:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_rename_hour_progressperhour_time_stamp_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Streak',
            new_name='Streaks',
        ),
    ]