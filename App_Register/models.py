from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import uuid
from . choices import HEARD_FROM


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class Register(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True, null=True, default="")
    last_name = models.CharField(max_length=100, blank=True, null=True, default="")
    email = LowercaseEmailField(max_length=100, blank=True, null=True, default='', unique=True)
    phone = models.CharField(max_length=100, blank=True, null=True, default="", unique=True)
    gender = models.BooleanField(default=False)
    technical_skill = models.BooleanField(default=False)
    heard_by = models.CharField(max_length=100, blank=True, null=True, choices=HEARD_FROM, default="")
    location = models.CharField(max_length=100, blank=True, null=True, default="")
    date_reg = models.DateTimeField(default=timezone.now)


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

