from django.urls import path

from .views import (
    create_category,
    create_post,
    create_thread,
    forum_category,
    forum_home,
    forum_thread,
)

app_name = "neighborhood"

urlpatterns = [
    path("", forum_home, name="forum_home"),
    path("thread/new/", create_thread, name="create_thread"),
    path("category/new/", create_category, name="create_category"),
    path("category/<slug:slug>/", forum_category, name="forum_category"),
    path("thread/<slug:slug>/", forum_thread, name="forum_thread"),
    path("thread/<slug:thread_slug>/reply/", create_post, name="create_post"),
]
