from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ForumPostForm, ThreadForm
from .models import ForumCategory, ForumPost, Thread


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
    return render(
        request,
        "forum_thread.html",
        {"thread": thread, "posts": posts},
    )


@login_required
def create_thread(request):
    if not request.user.is_authenticated or not (
        request.user.is_creator or request.user.is_superuser
    ):
        raise PermissionDenied("Only creators can create new threads.")

    if request.method == "POST":
        thread_form = ThreadForm(request.POST, prefix="thread")
        post_form = ForumPostForm(request.POST, prefix="post")

        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.author = request.user
            thread.save()

            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            post_form.save_m2m()

            return redirect("neighborhood:forum_thread", slug=thread.slug)
    else:
        thread_form = ThreadForm(prefix="thread")
        post_form = ForumPostForm(prefix="post")

    return render(
        request,
        "forum_create_thread.html",
        {
            "thread_form": thread_form,
            "post_form": post_form,
        },
    )


def create_post(request, thread_slug):
    thread = get_object_or_404(Thread, slug=thread_slug)

    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            form.save_m2m()  # Important for saving tags
            return redirect("neighborhood:forum_thread", slug=thread.slug)
    else:
        form = ForumPostForm()

    return render(
        request,
        "forum_create_post.html",
        {
            "form": form,
            "thread": thread,
        },
    )


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
