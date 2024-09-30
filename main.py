import logging

import click
from adapters.logger import setup_app_level_logger
import os
import django

# Set the environment variable to point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

# setup_sentry(settings.sentry)

setup_app_level_logger(
    name=__name__, level="DEBUG"
)


@click.group()
def cli():
    """
    Base cli function.
    """
    pass


@cli.command()
def run_core_business():
    from app.vps_core_business import run as run_core_business
    run_core_business()


@cli.command()
def run_schedular():
    from app.schedular import main as run_schedular
    run_schedular()


@cli.command()
def run_notify_consumer():
    from app.vps_notify_consumer import run as vps_notify_consumer
    vps_notify_consumer()


@cli.command()
def run_notification_gateway():
    from app.notification_gateway import run as notification_gateway
    notification_gateway()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info("Starting the app")
    cli()
