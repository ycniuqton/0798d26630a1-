# Generated by Django 4.2.9 on 2024-08-27 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_vpslog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpslog',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]