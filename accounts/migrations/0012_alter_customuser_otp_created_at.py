# Generated by Django 5.0 on 2024-01-03 15:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_customuser_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='otp_created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
