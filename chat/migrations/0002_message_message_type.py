# Generated by Django 5.0 on 2024-01-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('media', 'media')], null=True),
        ),
    ]