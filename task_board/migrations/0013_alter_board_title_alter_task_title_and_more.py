# Generated by Django 5.0 on 2024-01-02 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_board', '0012_alter_board_title_alter_task_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
