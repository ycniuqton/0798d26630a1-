# Generated by Django 4.2.9 on 2024-08-27 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_performed_by_vpslog_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vpslog',
            name='user',
        ),
    ]
