import random
import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("neighbor", "Neighbor"),
        ("creator", "Creator"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="neighbor")
    can_post = models.BooleanField(
        default=True
    )  # Allows easy blocking of posting privileges
    is_verified = models.BooleanField(default=False)  # Prevent login until confirmed
    verification_token = models.UUIDField(
        unique=True, null=True, blank=True
    )  # Temporarily allow null
    otp_code = models.CharField(
        max_length=6, blank=True, null=True
    )  # For OTP verification

    groups = models.ManyToManyField(
        Group,
        related_name="global_neighbor_users",  # Avoids conflicts with auth.User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="global_neighbor_user_permissions",  # Avoids conflicts with auth.User.user_permissions
        blank=True,
    )

    def is_neighbor(self):
        return self.role == "neighbor"

    def is_creator(self):
        return self.role == "creator"

    def generate_otp(self):
        """Generate a 6-digit OTP."""
        self.otp_code = str(random.randint(100000, 999999))
        self.save()
