# Generated by Django 5.0 on 2024-01-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customuser_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='otp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
