# Generated by Django 4.2.9 on 2024-08-28 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_invoice_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vps',
            old_name='end_date',
            new_name='end_time',
        ),
    ]
