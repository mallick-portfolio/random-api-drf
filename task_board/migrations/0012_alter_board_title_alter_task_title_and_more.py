# Generated by Django 5.0 on 2024-01-02 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_board', '0011_alter_taskitem_created_at_alter_taskitem_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='title',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]