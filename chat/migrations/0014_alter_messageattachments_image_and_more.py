# Generated by Django 5.0 on 2024-01-13 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_messageattachments_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageattachments',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='message/'),
        ),
        migrations.AlterField(
            model_name='messageattachments',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='message/'),
        ),
    ]
