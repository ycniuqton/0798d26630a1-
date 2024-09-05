from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vps, User, Balance


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
