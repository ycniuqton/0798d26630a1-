# Generated by Django 4.2.9 on 2024-09-12 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_vps_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='meta_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
