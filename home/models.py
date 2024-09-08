import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def gen_uuid():
    return str(uuid.uuid4())


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, default=gen_uuid, editable=False)
    _created = models.DateTimeField(auto_now_add=True)
    _updated = models.DateTimeField(auto_now=True)
    _deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def soft_delete(self):
        self._deleted = True
        self.save()

    def restore(self):
        self._deleted = False
        self.save()

    def save(self, *args, **kwargs):
        self._updated = timezone.now()
        super().save(*args, **kwargs)

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self._meta.fields}

    def to_readable_dict(self):
        def convert_build_in_types(value):
            if isinstance(value, (str, int, float, bool, list, dict)):
                return value
            if isinstance(value, timezone.datetime):
                return value.strftime("%d/%m/%Y")
            return str(value)

        return {field.name: convert_build_in_types(getattr(self, field.name)) for field in self._meta.fields}


class User(AbstractUser, BaseModel):
    id = models.CharField(primary_key=True, default=gen_uuid, editable=False)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country_region = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    subscribe_email = models.BooleanField(default=True)
    vps_len = models.PositiveIntegerField(default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_topup = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class VpsStatus:
    CREATING = "creating"
    ON = "on"
    OFF = "off"
    SUSPENDED = "suspended"
    SUSPENDING = "suspending"
    UNSUSPENDING = "unsuspending"
    SUSPENDED_NETWORK = "suspended_network"
    RESTARTING = "restarting"
    REBUILDING = "rebuilding"
    DELETING = "deleting"
    DELETED = "deleted"
    STOPPING = "stopping"
    STARTING = "starting"
    ERROR = "error"


class Vps(BaseModel):
    cpu = models.IntegerField(null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    disk = models.IntegerField(null=True, blank=True)
    network_speed = models.IntegerField(null=True, blank=True)
    bandwidth = models.IntegerField(null=True, blank=True)
    hostname = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    virt = models.CharField(max_length=20, null=True, blank=True)
    linked_id = models.IntegerField(null=True, blank=True)
    plan_id = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, default=VpsStatus.CREATING)
    os_version = models.CharField(max_length=200, null=True, blank=True)
    os = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)


    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname


class VPSLog(BaseModel):
    action = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    hostname = models.CharField(max_length=200)
    performed_by = models.CharField(max_length=200)
    description = models.TextField()
    vps = models.ForeignKey(Vps, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        # Automatically populate the hostname field from the related Vps instance
        if self.vps and not self.hostname:
            self.hostname = self.vps.hostname
        if self.user and not self.performed_by:
            self.performed_by = self.user.username
        super().save(*args, **kwargs)


class Balance(BaseModel):
    amount = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')

    def __str__(self):
        return f'{self.amount}'


class Transaction(BaseModel):
    amount = models.FloatField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    description = models.TextField()
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.amount} ({self.status})'


class Invoice(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=200, null=True, blank=True)
    cycle = models.CharField(max_length=200, null=True, blank=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='invoice', null=True,
                                       blank=True)

    def __str__(self):
        return f'{self.amount} ({self.status})'


class InvoiceLine(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines')
    description = models.TextField()
    amount = models.FloatField()
    status = models.CharField(max_length=200)
    vps = models.ForeignKey(Vps, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.amount} ({self.status})'


class Ticket(BaseModel):
    subject = models.CharField(max_length=200)
    ticket_type = models.CharField(max_length=200)
    description = models.TextField()
    submission_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200)
    operation = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class TicketChat(BaseModel):
    message = models.TextField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class UserToken(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    description = models.TextField()
    ttl = models.IntegerField()
    is_default = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token