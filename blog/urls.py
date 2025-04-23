from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BlogCategoryViewSet,
    BlogPostViewSet,
    blog_index,
    blog_post_detail,
    create_blog_post,
    delete_blog_post,
    edit_blog_post,
    edit_comment,
    like_comment,
    post_comment,
    tag_autocomplete,
    tag_suggestions,
    toggle_comment_like,
    toggle_post_like,
)

app_name = "blog"

router = DefaultRouter()
router.register(r"posts", BlogPostViewSet, basename="blogpost")
router.register(r"categories", BlogCategoryViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", blog_index, name="blog_index"),
    path("create/", create_blog_post, name="create_blog_post"),
    path("<slug:slug>/", blog_post_detail, name="blog_post_detail"),
    path("post/<slug:slug>/edit/", edit_blog_post, name="edit_blog_post"),
    path("post/<slug:slug>/comment/", post_comment, name="post_comment"),
    path("comment/<int:comment_id>/edit/", edit_comment, name="edit_comment"),
    path("post/<slug:slug>/delete/", delete_blog_post, name="delete_blog_post"),
    path("post/<int:post_id>/like/", toggle_post_like, name="toggle_post_like"),
    path(
        "comment/<int:comment_id>/like/",
        toggle_comment_like,
        name="toggle_comment_like",
    ),
    path("tags/suggest/", tag_suggestions, name="tag_suggestions"),
    path("api/tags/", tag_autocomplete, name="tag_autocomplete"),
]
