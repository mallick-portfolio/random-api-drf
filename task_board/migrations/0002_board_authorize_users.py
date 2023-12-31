# Generated by Django 5.0 on 2023-12-31 08:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_board', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='authorize_users',
            field=models.ManyToManyField(related_name='boards', to=settings.AUTH_USER_MODEL),
        ),
    ]