# Generated by Django 4.2.7 on 2023-11-06 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_word_alter_progress_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='card',
        ),
        migrations.AddField(
            model_name='progress',
            name='word',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.word'),
        ),
        migrations.DeleteModel(
            name='Vocabulary',
        ),
    ]
