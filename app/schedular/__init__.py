import os
import django

# Set the environment variable to point to your settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from app.schedular.jobs import UpdateVpsStat, CheckVPSExpired, CheckInvoiceExpired, CheckSuspendVPS, ArchiveVPS, \
    CollectReport, CheckTicketExpired


def main():
    # Instantiate the scheduler
    scheduler = BlockingScheduler()

    # Instantiate the job
    update_vps_stat = UpdateVpsStat()
    check_vps_expired = CheckVPSExpired()
    check_invoice_expired = CheckInvoiceExpired()
    check_vps_suspend = CheckSuspendVPS()
    check_expired_ticket = CheckTicketExpired()
    archive_vps = ArchiveVPS()
    collect_report = CollectReport()

    scheduler.add_job(update_vps_stat.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_vps_expired.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_invoice_expired.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_vps_suspend.run, 'cron', hour='*', minute='*')
    scheduler.add_job(archive_vps.run, 'cron', hour='*', minute='*')
    scheduler.add_job(collect_report.run, 'cron', hour='*', minute='*')
    scheduler.add_job(check_expired_ticket.run, 'cron', hour='*', minute='*')

    # Start the scheduler
    print("Starting scheduler...")
    scheduler.start()


if __name__ == '__main__':
    # job_instance = UpdateVpsStat()
    # job_instance.run()

    # check_vps_expired = CheckVPSExpired()
    # check_vps_expired.run()

    # check_expired_ticket = CheckTicketExpired()
    # check_expired_ticket.run()

    main()
