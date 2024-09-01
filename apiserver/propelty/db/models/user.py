# Python imports
import random
import string
import uuid

import pytz
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)

# Django imports
from django.db import models
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
        primary_key=True,
    )
    username = models.CharField(max_length=128, unique=True)
    # user fields
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )

    # identity
    display_name = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    avatar = models.TextField(blank=True)
    cover_image = models.URLField(blank=True, null=True, max_length=800)

    # tracking metrics
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Last Modified At"
    )
    last_location = models.CharField(max_length=255, blank=True)
    created_location = models.CharField(max_length=255, blank=True)

    # the is' es
    is_superuser = models.BooleanField(default=False)
    is_managed = models.BooleanField(default=False)
    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_password_autoset = models.BooleanField(default=False)

    # random token generated
    token = models.CharField(max_length=64, blank=True)

    last_active = models.DateTimeField(default=timezone.now, null=True)
    last_login_time = models.DateTimeField(null=True)
    last_logout_time = models.DateTimeField(null=True)
    last_login_ip = models.CharField(max_length=255, blank=True)
    last_logout_ip = models.CharField(max_length=255, blank=True)
    last_login_medium = models.CharField(
        max_length=20,
        default="email",
    )
    last_login_uagent = models.TextField(blank=True)
    token_updated_at = models.DateTimeField(null=True)
    # my_issues_prop = models.JSONField(null=True)

    is_bot = models.BooleanField(default=False)

    # timezone
    USER_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    user_timezone = models.CharField(
        max_length=255, default="UTC", choices=USER_TIMEZONE_CHOICES
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.username} <{self.email}>"

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        self.mobile_number = self.mobile_number

        if self.token_updated_at is not None:
            self.token = uuid.uuid4().hex + uuid.uuid4().hex
            self.token_updated_at = timezone.now()

        if not self.display_name:
            self.display_name = (
                self.email.split("@")[0]
                if len(self.email.split("@"))
                else "".join(
                    random.choice(string.ascii_letters) for _ in range(6)
                )
            )

        if self.is_superuser:
            self.is_staff = True

        super(User, self).save(*args, **kwargs)