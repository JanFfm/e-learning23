# Generated by Django 4.2.7 on 2023-11-23 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_timestamp'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timestamp',
            unique_together={('date', 'hour')},
        ),
    ]
