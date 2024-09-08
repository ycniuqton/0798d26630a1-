import os
import django

# Set the environment variable to point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from app.schedular.jobs import UpdateVpsStat


def main():
    # Instantiate the scheduler
    scheduler = BlockingScheduler()

    # Instantiate the job
    job_instance = UpdateVpsStat()

    scheduler.add_job(job_instance.run, 'cron', hour='*', minute='*')

    # Start the scheduler
    print("Starting scheduler...")
    scheduler.start()


if __name__ == '__main__':
    job_instance = UpdateVpsStat()
    job_instance.run()
    # main()
