# Generated by Django 5.0 on 2024-01-16 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_board', '0026_taskcomment_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcomment',
            name='comment_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]