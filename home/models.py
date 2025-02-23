import uuid
from datetime import datetime, timedelta

from django.db.models import JSONField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from config import APPConfig
from utils import generate_customer_code


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

        converting_fields = list(self._meta._property_names) + list([field.name for field in self._meta.fields])
        return {field: convert_build_in_types(getattr(self, field)) for field in converting_fields}


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
    open_ticket = models.PositiveIntegerField(default=0)
    customer_code = models.CharField(max_length=200, null=True, blank=True, default=generate_customer_code)

    class Meta:
        db_table = 'user'


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
    RESTORING = "restoring"
    REFUND_REQUESTED = "refund_requested"


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
    identifier = models.CharField(max_length=200, null=True, blank=True)
    meta_data = JSONField(null=True, blank=True)
    cycle = models.CharField(max_length=200, null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
    log_count = models.IntegerField(default=0)
    backup_count = models.IntegerField(default=0)
    region = JSONField(null=True, blank=True)
    creation_data = JSONField(null=True, blank=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname

    def is_expire_triggered(self):
        if not self.is_expired():
            return None
        event = TriggeredOnceEvent.objects.filter(event_name=TriggeredOnceEvent.EventName.VPS_EXPIRED,
                                                  vps_id=self.id, key=self.cycle).first()
        if event:
            return True
        return False

    def is_expired(self):
        return self.end_time < datetime.now(timezone.utc)

    @property
    def is_refundable(self):
        try:
            return self.end_time > self._created + timezone.timedelta(
                hours=APPConfig.VPS_REFUND_HOURS) > datetime.now(timezone.utc)
        except:
            return False

    class Meta:
        db_table = 'vps'

    @property
    def is_unpaid(self):
        unpaid_invoice_line = self.invoice_lines.filter(status=InvoiceLine.Status.OPEN).first()
        if unpaid_invoice_line:
            return True
        return False


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

    class Meta:
        db_table = 'vps_log'


class Balance(BaseModel):
    amount = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        db_table = 'balance'


class Transaction(BaseModel):
    amount = models.FloatField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    method = models.CharField(max_length=200, default='System')
    description = models.TextField()
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'transaction'


class Invoice(BaseModel):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        PAID = 'paid', 'Paid'
        CANCELED = 'canceled', 'Canceled'
        EXPIRED = 'expired', 'Expired'

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

    def is_expired(self):
        return self.due_date < datetime.now(timezone.utc)

    def is_expire_triggered(self):
        if not self.is_expired():
            return None
        event = TriggeredOnceEvent.objects.filter(event_name=TriggeredOnceEvent.EventName.INVOICE_EXPIRED,
                                                  invoice_id=self.id).first()
        if event:
            return True
        return False

    def is_suspend_triggered(self):
        event = TriggeredOnceEvent.objects.filter(event_name=TriggeredOnceEvent.EventName.INVOICE_SUSPENDED,
                                                  invoice_id=self.id).first()
        if event:
            return True
        return False

    @property
    def display_text(self):
        list_ip = []
        for line in self.lines.all():
            ip = line.vps.ip
            if ip is None:
                continue
            try:
                list_ip.append(ip)
            except:
                pass
        return ', '.join(list_ip)

    class Meta:
        db_table = 'invoice'


class InvoiceLine(BaseModel):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        PAID = 'paid', 'Paid'
        CANCELED = 'canceled', 'Canceled'
        EXPIRED = 'expired', 'Expired'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lines')
    description = models.TextField()
    amount = models.FloatField()
    status = models.CharField(max_length=200, default=Status.OPEN)
    vps = models.ForeignKey(Vps, on_delete=models.CASCADE, related_name='invoice_lines')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    cycle = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'invoice_line'


class Ticket(BaseModel):
    class TicketStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'
        EXPIRED = 'expired', 'Expired'
        UNREAD = 'unread', 'Unread'

    subject = models.CharField(max_length=200)
    ticket_type = models.CharField(max_length=200)
    description = models.TextField()
    submission_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, choices=TicketStatus.choices, default=TicketStatus.UNREAD)
    operation = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    attached_vps = JSONField(null=True, blank=True)
    attached_invoice = JSONField(null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'ticket'


class TicketChat(BaseModel):
    message = models.TextField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'ticket_chat'


class UserToken(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    description = models.TextField()
    ttl = models.IntegerField()
    is_default = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token

    class Meta:
        db_table = 'user_token'


class PaypalTransaction(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        PAID = 'A', 'Paid'
        CANCELED = 'C', 'Canceled'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.FloatField()
    currency = models.CharField(max_length=200, default='USD')
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.PENDING)
    description = models.TextField()
    payment_id = models.CharField(max_length=200)
    token = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'paypal_transaction'


class CryptoTransaction(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        PAID = 'A', 'Paid'
        UNKNOWN = 'U', 'Unknown'
        CANCELED = 'C', 'Canceled'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=200, default='USD')
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.PENDING)
    description = models.TextField()
    payment_id = models.CharField(max_length=200, unique=True)
    raw_data = JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'crypto_transaction'


class StripeTransaction(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        PAID = 'A', 'Paid'
        UNKNOWN = 'U', 'Unknown'
        CANCELED = 'C', 'Canceled'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=200, default='USD')
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.PENDING)
    description = models.TextField()
    payment_id = models.CharField(max_length=200, unique=True)
    raw_data = JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'stripe_transaction'


class BankTransaction(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        PAID = 'A', 'Paid'
        CANCELED = 'C', 'Canceled'
        UNDEFINED = 'U', 'Undefined'

    class Gateway(models.TextChoices):
        BIDV = 'BIDV', 'BIDV'
        VIETCOMBANK = 'VIETCOMBANK', 'Vietcombank'
        TECHCOMBANK = 'TECHCOMBANK', 'Techcombank'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=200, default='VND')
    status = models.CharField(max_length=200, choices=Status.choices, default=Status.PENDING)
    description = models.TextField()
    gateway = models.CharField(max_length=200, choices=Gateway.choices, default=Gateway.BIDV)
    payment_id = models.CharField(max_length=200)
    raw_data = JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'bank_transaction'


class TriggeredOnceEvent(BaseModel):
    class EventName(models.TextChoices):
        VPS_EXPIRED = 'VPS_EXPIRED', 'VPS Expired'
        INVOICE_EXPIRED = 'INVOICE_EXPIRED', 'Invoice Expired'
        INVOICE_SUSPENDED = 'INVOICE_SUSPENDED', 'Invoice Suspended'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event_name = models.CharField(max_length=200, choices=EventName.choices, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, blank=True)
    vps_id = models.CharField(max_length=200, null=True, blank=True)
    invoice_id = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    triggered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'triggered_once_event'


class AppSetting(BaseModel):
    invoice_due_days = models.IntegerField(default=3)
    sufficient_balance_suspend_days = models.IntegerField(default=0)
    vps_auto_archive = models.IntegerField(default=0)
    vps_refund_hours = models.IntegerField(default=0)
    group_locked_config = JSONField(default=dict)

    class Meta:
        db_table = 'app_setting'


class RefundRequest(BaseModel):
    class RefundRequestStatus:
        PENDING = 'pending'
        APPROVED = 'approved'
        REJECTED = 'rejected'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=200, default=RefundRequestStatus.PENDING)
    description = models.TextField()
    vps = models.ForeignKey(Vps, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.amount} ({self.status})'

    class Meta:
        db_table = 'refund_request'


class TopUpReport(BaseModel):
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.amount} ({self.date})'

    class Meta:
        db_table = 'topup_report'


class InvoicePaidReport(BaseModel):
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.amount} ({self.date})'

    class Meta:
        db_table = 'invoice_paid_report'


class OrderReport(BaseModel):
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.amount} ({self.date})'

    class Meta:
        db_table = 'order_report'


class UnpaidOrderReport(BaseModel):
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.amount} ({self.date})'

    class Meta:
        db_table = 'unpaid_order_report'


class RefundReport(BaseModel):
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.amount} ({self.date})'

    class Meta:
        db_table = 'refund_report'


class SystemCounter(BaseModel):
    class CounterType(models.TextChoices):
        VPS = 'VPS', 'VPS'

    class KEYGEN:
        @staticmethod
        def vps(obj=None, plan_id=None):
            if obj:
                return f"vps_id:{obj.id}"
            if plan_id:
                return f"plan_id:{plan_id}"
            raise ValueError("Invalid arguments")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    data = JSONField(default=dict)
    type = models.CharField(max_length=200, choices=CounterType.choices, default=CounterType.VPS)

    @staticmethod
    def get_vps_counter(user, plan_id):
        counter = SystemCounter.objects.filter(user=user, type=SystemCounter.CounterType.VPS).first()
        if not counter:
            return 0
        return counter.data.get(SystemCounter.KEYGEN.vps(plan_id=plan_id), 0)


class VNCSession(models.Model):
    vps = models.ForeignKey(Vps, on_delete=models.CASCADE, related_name='vnc_sessions', unique=True)
    password = models.CharField(max_length=200)
    port = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    session_key = models.CharField(max_length=200, unique=True)
    vnc_link = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vnc_session'

    def __str__(self):
        return f"VNC Session for VPS {self.vps.hostname} - Port: {self.port}"

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() < self.expired_at


class PendingRegistration(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Will store hashed password
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    resend_count = models.IntegerField(default=0)
    last_resend_at = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)
    last_failed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set expiration to 24 hours from creation
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def can_resend_email(self):
        """Check if confirmation email can be resent based on rate limits"""
        if self.resend_count >= 5:  # Max 5 resends total
            return False
            
        if self.last_resend_at:
            # Must wait 2 minutes between resends
            min_interval = timedelta(minutes=2)
            if timezone.now() - self.last_resend_at < min_interval:
                return False
                
        return True

    def increment_failed_attempts(self):
        """Track failed confirmation attempts"""
        self.failed_attempts += 1
        self.last_failed_at = timezone.now()
        self.save()

    def is_blocked(self):
        """Check if registration is blocked due to too many failed attempts"""
        if self.failed_attempts >= 5:  # Max 5 failed attempts
            if self.last_failed_at:
                # Block for 30 minutes after 5 failed attempts
                block_duration = timedelta(minutes=30)
                if timezone.now() - self.last_failed_at < block_duration:
                    return True
            return False
        return False

    class Meta:
        db_table = 'pending_registrations'
