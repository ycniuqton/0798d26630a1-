# Generated by Django 4.2.9 on 2024-09-03 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_ticketchat_ticket_alter_ticketchat_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpslog',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
