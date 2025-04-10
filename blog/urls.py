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
    path("comment/<int:comment_id>/like/", like_comment, name="like_comment"),
    path("comment/<int:comment_id>/edit/", edit_comment, name="edit_comment"),
    path("post/<slug:slug>/delete/", delete_blog_post, name="delete_blog_post"),
]
