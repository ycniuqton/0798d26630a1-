# Generated by Django 4.2.9 on 2024-08-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_invoice_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cycle',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]