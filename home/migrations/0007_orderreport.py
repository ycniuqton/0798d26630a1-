# Generated by Django 4.2.9 on 2024-10-06 15:07

from django.db import migrations, models
import django.utils.timezone
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_invoicepaidreport_refundreport_topupreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderReport',
            fields=[
                ('id', models.CharField(default=home.models.gen_uuid, editable=False, primary_key=True, serialize=False)),
                ('_created', models.DateTimeField(auto_now_add=True)),
                ('_updated', models.DateTimeField(auto_now=True)),
                ('_deleted', models.BooleanField(default=False)),
                ('amount', models.FloatField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'order_report',
            },
        ),
    ]
