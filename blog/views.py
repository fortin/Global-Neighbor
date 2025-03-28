from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .forms import BlogPostForm  # You'll need to create this form
from .models import BlogCategory, BlogPost
from .serializers import BlogCategorySerializer, BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()  # .order_by("-created_at")
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


def is_creator(user):
    return user.is_authenticated and (user.is_creator or user.is_superuser)


@login_required
@user_passes_test(is_creator)
def create_blog_post(request):
    """Allow only Creators to add a new blog post."""
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:blog_index")  # Redirect to blog index after posting
    else:
        form = BlogPostForm()

    return render(request, "create_blog_post.html", {"form": form})


def blog_index(request):
    posts = BlogPost.objects.all()  # .order_by("-created_at")
    return render(request, "blog_index.html", {"posts": posts})


def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog_post.html", {"post": post})


@login_required
def edit_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.user != post.author and not request.user.is_superuser:
        raise PermissionDenied()

    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)  # Ensure slug is updated
            post.save()
            form.save_m2m()
            return redirect("blog:blog_post_detail", slug=post.slug)
    else:
        form = BlogPostForm(instance=post)

    return render(request, "edit_blog_post.html", {"form": form, "post": post})
