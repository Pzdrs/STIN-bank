# Generated by Django 4.2 on 2023-04-12 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_use_2fa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pending_verification',
            field=models.BooleanField(default=False),
        ),
    ]
