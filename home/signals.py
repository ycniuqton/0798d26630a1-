from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from adapters.kafka_adapter import make_kafka_publisher
from config import NotificationGatewayConfig
from .models import Vps, User, Balance, Transaction, Ticket, VPSLog, TicketChat


@receiver(post_save, sender=Vps)
def trigger_when_vps_created(sender, instance, created, **kwargs):
    if created:  # Only publish when the instance is created
        publisher = make_kafka_publisher(NotificationGatewayConfig)
        publisher.publish('vps_created', {'vps_id': instance.id})


@receiver(post_delete, sender=Vps)
def update_vps_len_on_delete(sender, instance, **kwargs):
    user = instance.user  # Assuming there is a ForeignKey from VPS to User
    user.vps_len = Vps.objects.filter(user=user).count()  # Count user's VPS instances
    user.save()


@receiver(post_save, sender=Balance)
def update_balance_amount_on_save(sender, instance, **kwargs):
    user = instance.user
    user.balance_amount = instance.amount
    user.save()


@receiver(post_save, sender=Transaction)
def update_account_statistic_on_save(sender, instance, **kwargs):
    user = instance.user
    total_paid = Transaction.objects.filter(user=user, type='charge').aggregate(Sum('amount'))['amount__sum']
    if total_paid:
        user.total_paid = - total_paid
    total_topup = Transaction.objects.filter(user=user, type='topup').aggregate(Sum('amount'))['amount__sum']
    if total_topup:
        user.total_topup = total_topup
    user.save()


@receiver(post_save, sender=Ticket)
def update_ticket_len_on_save(sender, instance, **kwargs):
    user = instance.user
    user.open_ticket = Ticket.objects.filter(user=user, status=Ticket.TicketStatus.OPEN).count()
    user.save()


@receiver(post_save, sender=VPSLog)
def update_vps_log_counter(sender, instance, **kwargs):
    vps = instance.vps
    vps.log_count = VPSLog.objects.filter(vps=vps).count()
    vps.save()


@receiver(post_save, sender=TicketChat)
def update_ticket_status(sender, instance, **kwargs):
    ticket = instance.ticket
    if instance.user.is_staff:
        ticket.status = Ticket.TicketStatus.OPEN
    else:
        ticket.status = Ticket.TicketStatus.UNREAD
    ticket.save()