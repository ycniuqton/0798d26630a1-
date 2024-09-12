from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vps, User, Balance, Transaction


@receiver(post_save, sender=Vps)
def update_vps_len_on_save(sender, instance, **kwargs):
    user = instance.user  # Assuming there is a ForeignKey from VPS to User
    user.vps_len = Vps.objects.filter(user=user).count()  # Count user's VPS instances
    user.save()


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
