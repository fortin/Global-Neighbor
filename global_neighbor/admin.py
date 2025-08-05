from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Document, DocumentCategory, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Permissions", {"fields": ("role", "can_post")}),
    )

    list_display = ("username", "email", "role", "can_post")
    list_filter = ("role", "can_post")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category")


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
