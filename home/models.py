import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def gen_uuid():
    return str(uuid.uuid4())


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=gen_uuid, editable=False)
    pass


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
                return value.isoformat()
            return str(value)

        return {field.name: convert_build_in_types(getattr(self, field.name)) for field in self._meta.fields}


class VpsStatus:
    CREATING = "creating"
    ON = "on"
    OFF = "off"
    SUSPENDED = "suspended"
    SUSPENDED_NETWORK = "suspended_network"


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
    os = models.CharField(max_length=200, null=True, blank=True)

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
    vps = models.ForeignKey(Vps, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        # Automatically populate the hostname field from the related Vps instance
        if self.vps and not self.hostname:
            self.hostname = self.vps.hostname
        if self.user and not self.performed_by:
            self.performed_by = self.user.username
        super().save(*args, **kwargs)
