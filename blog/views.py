import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from taggit.models import Tag

from .forms import BlogPostForm  # You'll need to create this form
from .forms import BlogCommentForm
from .models import BlogCategory, BlogComment, BlogPost
from .serializers import BlogCategorySerializer, BlogPostSerializer

logger = logging.getLogger(__name__)


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
    comments = (
        post.comments.filter(parent__isnull=True)
        .select_related("author")
        .prefetch_related("replies", "likes")
    )

    if request.method == "POST" and request.user.is_authenticated:
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent_id = int(parent_id)

            comment.save()

            # Send notification to parent comment author (if not self)
            if comment.parent and comment.parent.author != request.user:
                send_mail(
                    subject="New reply to your comment",
                    message=f"{request.user} replied to your comment on '{post.title}'",
                    from_email="no-reply@globalneighbor.com",
                    recipient_list=[comment.parent.author.email],
                    fail_silently=True,
                )

            return redirect("blog:blog_post_detail", slug=slug)
    else:
        form = BlogCommentForm()

    return render(
        request,
        "blog_post.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": form,
        },
    )


@login_required
def edit_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.user != post.author and not (
        request.user.is_superuser or request.user.is_moderator
    ):
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


@login_required(login_url="login")
def post_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:blog_post_detail", slug=slug)
    return redirect("blog:blog_post_detail", slug=slug)


@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(BlogComment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(BlogComment, id=comment_id)

    if request.user != comment.author and not (
        request.user.is_superuser or request.user.is_moderator
    ):
        raise PermissionDenied()

    if request.method == "POST":
        form = BlogCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:blog_post_detail", slug=comment.post.slug)
    else:
        form = BlogCommentForm(instance=comment)

    return render(request, "edit_comment.html", {"form": form, "comment": comment})


@login_required
def delete_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.user != post.author and not (
        request.user.is_superuser or request.user.is_moderator()
    ):
        raise PermissionDenied()

    if request.method == "POST":
        post.delete()
        return redirect(
            "blog:blog_index"
        )  # Or wherever you want to redirect after deletion

    # Optional: if you want a confirmation page
    return redirect("blog:blog_post_detail", slug=slug)


@login_required
@require_POST
def toggle_post_like(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()})


@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(BlogComment, id=comment_id)

    if request.method == "POST":
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"liked": liked, "likes_count": comment.likes.count()})
        else:
            return redirect(comment.post.get_absolute_url())
    return HttpResponseBadRequest("Invalid request.")


@require_GET
def tag_suggestions(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)

    tags = Tag.objects.filter(name__icontains=q).values_list("name", flat=True)[:10]
    return JsonResponse(list(tags), safe=False)


def tag_autocomplete(request):
    q = request.GET.get("q", "").strip()
    suggestions = list(
        Tag.objects.filter(name__istartswith=q)
        .values_list("name", flat=True)
        .distinct()
    )[:10]
    return JsonResponse(suggestions, safe=False)
