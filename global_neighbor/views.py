import random
import uuid

from decouple import config
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import localtime
from taggit.models import Tag

from blog.models import BlogCategory, BlogPost
from global_neighbor.bluesky import get_latest_bluesky_posts
from neighborhood.models import ForumPost, Thread

from .bluesky_utils import get_latest_top_level_posts
from .forms import RegistrationForm
from .models import User


def home(request):
    bluesky_posts, bsky_display_name = get_latest_top_level_posts()
    latest_blog_posts = BlogPost.objects.order_by("-created")[:5]
    latest_forum_posts = ForumPost.objects.order_by("-created")[:5]
    bsky_handle = config("BLUESKY_USERNAME")

    blog_digest = [
        {
            "timestamp": localtime(post.created).strftime("%b %d, %Y %H:%M"),
            "text": post.title,
            "url": reverse("blog:blog_post_detail", kwargs={"slug": post.slug}),
        }
        for post in latest_blog_posts
    ]

    forum_digest = [
        {
            "timestamp": localtime(post.created).strftime("%b %d, %Y %H:%M"),
            "text": post.thread.title,
            "url": reverse(
                "neighborhood:forum_thread", kwargs={"slug": post.thread.slug}
            ),
        }
        for post in latest_forum_posts
    ]

    context = {
        "bluesky_posts": bluesky_posts,
        "latest_blog_posts": blog_digest,
        "latest_forum_posts": forum_digest,
        "bsky_handle": bsky_handle,
        "bsky_name": bsky_display_name,
    }

    return render(request, "home.html", context)


def generate_otp(self):
    self.otp = str(random.randint(100000, 999999))
    self.verification_token = uuid.uuid4()  # Ensure a valid UUID
    self.save()


def register(request):
    """Handles user registration and sends verification email."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.generate_otp()  # Ensure this sets verification_token

            if not user.verification_token:  # Debugging step
                print("Error: verification_token is missing!")

            send_verification_email(
                request, user
            )  # Ensure the token is set before this

            return redirect("confirm_registration")  # Redirect to OTP input page
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def send_verification_email(request, user, verify_url=None):
    """Sends an email with a verification link and OTP."""

    # Get full domain from request
    domain = request.get_host()
    scheme = "https" if request.is_secure() else "http"

    # Build verification link if not passed in
    if not verify_url:
        token = str(user.verification_token)
        verify_url = f"{scheme}://{domain}{reverse('verify_email', args=[token])}"

    subject = "Confirm Your Registration"

    otp = getattr(user, "otp", None)
    otp_display = otp if otp else "⚠️ Not set"

    message = f"""
    Welcome to Global Neighbor!

    Please verify your account using one of the methods below:

    - Click the link: {verify_url}
    - Enter the following OTP: {otp_display}

    Thank you!
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def confirm_registration(request):
    """Display OTP confirmation form."""
    if request.method == "POST":
        otp = request.POST.get("otp", "").strip()
        user = User.objects.filter(otp=otp, is_verified=False).first()
        if user:
            user.is_verified = True
            user.is_active = True  # Allow authentication
            user.otp_code = None
            user.save()
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "registration/confirm_registration.html",
                {"error": "Invalid OTP"},
            )

    return render(request, "registration/confirm_registration.html")


def verify_email(request, token):
    """Activate user via email link."""
    user = get_object_or_404(User, verification_token=token, is_verified=False)
    user.is_verified = True
    user.is_active = True  # Allow authentication
    user.save()
    login(request, user)
    return redirect("home")


def search(request):
    query = request.GET.get("q", "")
    blog_results = BlogPost.objects.filter(content__icontains=query)
    forum_posts = ForumPost.objects.filter(content__icontains=query)
    forum_threads = Thread.objects.filter(title__icontains=query)
    return render(
        request,
        "search/search_results.html",
        {
            "query": query,
            "blog_results": blog_results,
            "forum_posts": forum_posts,
            "forum_threads": forum_threads,
        },
    )


def advanced_search(request):
    query = request.GET.get("q", "").strip()
    scope = request.GET.get("scope", "")
    selected_tag = request.GET.get("tag", "")
    selected_category = request.GET.get("category", "")

    blog_results = BlogPost.objects.all()
    forum_threads = Thread.objects.all()
    forum_posts = ForumPost.objects.all()
    tags = Tag.objects.all()
    categories = BlogCategory.objects.all().values_list("name", flat=True)

    def parse_query(text):
        terms = text.split()
        q = Q()
        current_op = Q.__or__

        for term in terms:
            if term.upper() == "AND":
                current_op = Q.__and__
            elif term.upper() == "OR":
                current_op = Q.__or__
            elif term.upper() == "NOT" or term.startswith("-"):
                term = (
                    term[1:]
                    if term.startswith("-")
                    else terms.pop(terms.index(term) + 1)
                )
                q &= ~Q(name__icontains=term) & ~Q(content__icontains=term)
            else:
                term = term[1:] if term.startswith("+") else term
                q = current_op(q, Q(name__icontains=term) | Q(content__icontains=term))
        return q

    if query:
        q_filter = parse_query(query)

        tag_string = request.GET.get("tags", "").strip()
        if tag_string:
            tag_list = [tag.strip() for tag in tag_string.split(",") if tag.strip()]
            if tag_list:
                if scope in ("", "blog"):
                    blog_results = blog_results.filter(
                        tags__name__in=tag_list
                    ).distinct()
                if scope in ("", "forum"):
                    forum_posts = forum_posts.filter(tags__name__in=tag_list).distinct()

    return render(
        request,
        "search/advanced_search.html",
        {
            "query": query,
            "scope": scope,
            "selected_tag": selected_tag,
            "selected_category": selected_category,
            "tags": tags,
            "categories": categories,
            "blog_results": blog_results,
            "forum_threads": forum_threads,
            "forum_posts": forum_posts,
        },
    )


@login_required()
def search_results(request):
    query = request.GET.get("q", "").strip()
    blog_results = []
    forum_threads = []
    forum_posts = []

    if query:
        blog_results = BlogPost.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

        forum_threads = Thread.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

        forum_posts = ForumPost.objects.filter(
            Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    return render(
        request,
        "search/search_results.html",
        {
            "query": query,
            "blog_results": blog_results,
            "forum_threads": forum_threads,
            "forum_posts": forum_posts,
        },
    )
