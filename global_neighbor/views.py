import json
import random
import uuid

from decouple import config
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from taggit.models import Tag

from blog.models import BlogCategory, BlogPost, User
from global_neighbor.bluesky import get_latest_bluesky_posts
from global_neighbor.models import Document, DocumentCategory
from neighborhood.models import ForumPost, Thread

from .bluesky_utils import get_latest_top_level_posts
from .forms import DocumentForm, DocumentUploadForm, RegistrationForm


def is_creator(user):
    return user.is_authenticated and user.role == "creator"


def is_neighbor(user):
    return user.is_authenticated and user.role == "neighbor"


def home(request):
    bluesky_posts, bsky_display_name = get_latest_top_level_posts()
    latest_blog_posts = BlogPost.objects.order_by("-created")[:5]
    latest_forum_posts = ForumPost.objects.order_by("-created")[:5]
    latest_documents = Document.objects.order_by("-uploaded_at")[:2]
    bsky_handle = config("BLUESKY_USERNAME")

    blog_digest = [
        {
            "timestamp": localtime(post.created).strftime("%b %d, %Y %H:%M"),
            "text": post.title,
            "url": reverse("blog:blog_post_detail", kwargs={"slug": post.slug}),
        }
        for post in latest_blog_posts
    ][
        :2
    ]  # limit to 2 after digest is built

    forum_digest = [
        {
            "timestamp": localtime(post.created).strftime("%b %d, %Y %H:%M"),
            "text": post.thread.title,
            "url": reverse(
                "neighborhood:forum_thread", kwargs={"slug": post.thread.slug}
            ),
        }
        for post in latest_forum_posts
    ][
        :2
    ]  # limit to 2 after digest is built

    context = {
        "bluesky_posts": bluesky_posts,
        "latest_blog_posts": blog_digest,
        "latest_forum_posts": forum_digest,
        "latest_documents": latest_documents,
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
    query = request.GET.get("q") or request.GET.get("search") or ""
    scope = request.GET.get("scope")
    tags = request.GET.get("tags", "")
    category = request.GET.get("category")

    blog_results = []
    forum_threads = []
    forum_posts = []

    if query.strip():
        if not scope or scope == "all" or scope == "blog":
            blog_results = BlogPost.objects.filter(title__icontains=query)

        if not scope or scope == "all" or scope == "forum":
            forum_threads = Thread.objects.filter(title__icontains=query)
            forum_posts = ForumPost.objects.filter(content__icontains=query)

        # Optional: filter by tag or category here
        # if tags: ...
        # if category: ...

    context = {
        "query": query,
        "scope": scope,
        "blog_results": blog_results,
        "forum_threads": forum_threads,
        "forum_posts": forum_posts,
    }

    return render(request, "search/advanced_search.html", context)


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


@login_required
@user_passes_test(lambda u: u.role == "creator" or u.is_superuser)
def upload_document(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    uploaded_file = request.FILES.get("file")  # ✅ Ensure input name="file"
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    title = request.POST.get("title", "").strip() or "Untitled Document"
    author = request.POST.get("author", "").strip()
    source = request.POST.get("source", "").strip()
    category_id = request.POST.get("category")
    tag_string = request.POST.get("tags", "")

    # Process category if applicable
    category = None
    if category_id:
        from .models import DocumentCategory  # adjust import as needed

        try:
            category = DocumentCategory.objects.get(id=category_id)
        except DocumentCategory.DoesNotExist:
            pass  # silently fail or handle as needed

    # Create document entry
    document = Document.objects.create(
        title=title,
        author=author,
        source=source,
        file=uploaded_file,
        uploaded_by=request.user,
        category=category,
    )

    # Handle tags
    if tag_string:
        tag_names = [t.strip() for t in tag_string.split(",") if t.strip()]
        document.tags.set(tag_names)

    return JsonResponse({"status": "ok", "document_id": document.id})


def library(request):
    documents = Document.objects.all()
    categories = DocumentCategory.objects.all()

    context = {
        "documents": documents,
        "categories": categories,
    }
    return render(request, "library/library.html", context)


@login_required
@user_passes_test(is_neighbor)
def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.download_count += 1
    document.save(update_fields=["download_count"])
    try:
        return FileResponse(
            document.file.open("rb"), as_attachment=True, filename=document.file.name
        )
    except FileNotFoundError:
        raise Http404("Document not found.")


def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    return render(request, "library/document_detail.html", {"document": doc})


def edit_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        form = DocumentForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            return redirect("library")  # Redirect to Library after saving
    else:
        form = DocumentForm(instance=doc)

    return render(
        request, "library/edit_document.html", {"form": form, "document": doc}
    )


@login_required
@user_passes_test(lambda u: u.role == "creator" or u.is_superuser)
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        document.delete()
        return redirect("library")  # Redirect back to Library page

    # Optional: Show a confirmation page
    return render(request, "library/confirm_delete.html", {"document": document})


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    data = json.loads(request.body)
    name = data.get("name")
    if name:
        DocumentCategory.objects.create(name=name)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Name required"}, status=400)


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, pk):
    try:
        DocumentCategory.objects.get(pk=pk).delete()
        return JsonResponse({"status": "ok"})
    except DocumentCategory.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
