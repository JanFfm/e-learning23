# Generated by Django 4.2.7 on 2023-11-13 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_progress_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence_en', models.CharField(max_length=500)),
                ('sentence_de', models.CharField(max_length=500)),
            ],
        ),
    ]
