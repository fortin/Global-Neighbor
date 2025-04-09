from django.contrib import admin

from neighborhood.models import ForumCategory


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
