# Generated by Django 4.2.9 on 2024-09-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_paypaltransaction_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='method',
            field=models.CharField(default='System', max_length=200),
        ),
    ]