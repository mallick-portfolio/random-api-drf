# Generated by Django 5.0 on 2024-01-04 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_board', '0017_alter_board_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
