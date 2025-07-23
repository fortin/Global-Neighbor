import random
import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    ROLE_CHOICES = [
        ("neighbor", "Neighbor"),
        ("creator", "Creator"),
        ("moderator", "Moderator"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="neighbor")
    can_post = models.BooleanField(
        default=True
    )  # Allows easy blocking of posting privileges
    is_verified = models.BooleanField(default=False)  # Prevent login until confirmed
    verification_token = models.CharField(
        max_length=64,
        unique=True,
        default=uuid.uuid4,  # Ensures a valid default
    )
    otp = models.CharField(max_length=6, blank=True, null=True)

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

    def is_moderator(self):
        return self.role == "moderator"

    def generate_otp(self):
        """Generates OTP and ensures the user has a valid UUID verification token."""

        self.otp = str(random.randint(100000, 999999))

        # Ensure verification token is set correctly
        if not self.verification_token:
            self.verification_token = uuid.uuid4()  # ✅ Proper UUID

        self.save()


class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = TaggableManager(blank=True)

    file = models.FileField(upload_to="documents/")
    uploaded_by = models.ForeignKey("global_neighbor.User", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
