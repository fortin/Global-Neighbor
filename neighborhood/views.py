from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, PostForm, ThreadForm
from .models import ForumCategory, Post, Thread


def forum_home(request):
    categories = ForumCategory.objects.all()
    return render(request, "forum_home.html", {"categories": categories})


def forum_category(request, slug):
    category = get_object_or_404(ForumCategory, slug=slug)
    threads = category.threads.all()
    return render(
        request, "forum_category.html", {"category": category, "threads": threads}
    )


def forum_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    posts = thread.posts.all()
    return render(request, "forum_thread.html", {"thread": thread, "posts": posts})


@login_required
def create_thread(request):
    if not request.user.is_authenticated or (
        request.user.is_neighbor()
        or request.user.is_creator()
        or request.user.is_superuser()
    ):
        raise PermissionDenied("Only creators can create new threads.")

    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect("forum_thread", slug=thread.slug)
    else:
        form = ThreadForm()
    return render(request, "forum_create_thread.html", {"form": form})


def create_post(request, thread_slug):
    thread = get_object_or_404(Thread, slug=thread_slug)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            return redirect("forum_thread", slug=thread.slug)
    else:
        form = PostForm()
    return render(request, "forum_create_post.html", {"form": form, "thread": thread})


@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("neighborhood:forum_home")
    else:
        form = CategoryForm()

    return render(request, "forum_create_category.html", {"form": form})
