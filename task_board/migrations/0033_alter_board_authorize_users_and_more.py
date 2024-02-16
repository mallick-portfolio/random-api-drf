# Generated by Django 5.0 on 2024-02-16 11:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_board', '0032_alter_board_authorize_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='authorize_users',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='task',
            name='authorize_users',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20, null=True), blank=True, null=True, size=None),
        ),
    ]
