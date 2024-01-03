# Generated by Django 5.0 on 2024-01-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_customuser_created_at_customuser_otp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='created_at',
            new_name='otp_created_at',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_email_verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
