# Generated by Django 4.1 on 2023-11-26 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_progressperhour_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ('lection', 'word')},
        ),
    ]
