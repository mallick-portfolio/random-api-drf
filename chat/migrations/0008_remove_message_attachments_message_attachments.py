# Generated by Django 5.0 on 2024-01-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_remove_messageattachments_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='attachments',
        ),
        migrations.AddField(
            model_name='message',
            name='attachments',
            field=models.JSONField(blank=True, null=True),
        ),
    ]