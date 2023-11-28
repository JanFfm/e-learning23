# Generated by Django 4.2.7 on 2023-11-25 16:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_merge_20231124_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='progressperhour',
            options={'ordering': ('user', 'time_stamp')},
        ),
        migrations.RemoveField(
            model_name='progressperhour',
            name='correct_sentence_count',
        ),
        migrations.RemoveField(
            model_name='progressperhour',
            name='correct_word_count',
        ),
        migrations.RemoveField(
            model_name='progressperhour',
            name='sentence_count',
        ),
        migrations.RemoveField(
            model_name='progressperhour',
            name='word_count',
        ),
        migrations.AddField(
            model_name='progressperhour',
            name='correct_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='progressperhour',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lectionprogress',
            name='progress',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
