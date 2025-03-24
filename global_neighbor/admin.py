from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Permissions", {"fields": ("role", "can_post")}),
    )

    list_display = ("username", "email", "role", "can_post")
    list_filter = ("role", "can_post")


admin.site.register(User, CustomUserAdmin)
