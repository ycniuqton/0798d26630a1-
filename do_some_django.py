import logging

import click
from adapters.logger import setup_app_level_logger
import os
import django


# Set the environment variable to point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()
from services.app_setting import AppSettingRepository


app_setting = AppSettingRepository()
app_setting.INVOICE_DUE_DAYS = 1
app_setting.SUFFICIENT_BALANCE_SUSPEND_DAYS = 0
