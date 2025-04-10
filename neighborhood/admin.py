from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from neighborhood.models import ForumCategory


@admin.register(ForumCategory)
class ForumCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "parent",
        "sort_order",
    )
    list_editable = ("sort_order",)
    ordering = ("sort_order",)
