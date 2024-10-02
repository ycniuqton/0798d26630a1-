import os
import django

# Set the environment variable to point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from app.schedular.jobs import UpdateVpsStat, CheckVPSExpired, CheckInvoiceExpired, CheckSuspendVPS


def main():
    # Instantiate the scheduler
    scheduler = BlockingScheduler()

    # Instantiate the job
    update_vps_stat = UpdateVpsStat()
    check_vps_expired = CheckVPSExpired()
    check_invoice_expired = CheckInvoiceExpired()
    check_vps_suspend = CheckSuspendVPS()

    scheduler.add_job(update_vps_stat.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_vps_expired.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_invoice_expired.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_vps_suspend.run, 'cron', hour='*', minute='*')

    # Start the scheduler
    print("Starting scheduler...")
    scheduler.start()


if __name__ == '__main__':
    # job_instance = UpdateVpsStat()
    # job_instance.run()

    # check_vps_expired = CheckVPSExpired()
    # check_vps_expired.run()

    main()
