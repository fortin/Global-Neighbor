from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import RegistrationForm
from .models import User


def home(request):
    """Render the portal home page."""
    return render(request, "home.html")


def register(request):
    """Handles user registration and sends verification email."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.generate_otp()  # Generate OTP for verification
            send_verification_email(request, user)
            return redirect("confirm_registration")  # Redirect to OTP input page
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def send_verification_email(request, user):
    """Send verification email with token and OTP."""
    subject = "Confirm Your Registration"
    site = get_current_site(request)
    verify_url = (
        f"http://{site.domain}{reverse('verify_email', args=[user.verification_token])}"
    )

    message = f"""
    Welcome to Global Neighbor!

    Please verify your account using one of the methods below:

    - Click the link: {verify_url}
    - Enter the following OTP: {user.otp_code}

    Thank you!
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def confirm_registration(request):
    """Display OTP confirmation form."""
    if request.method == "POST":
        otp = request.POST.get("otp")
        user = User.objects.filter(otp_code=otp, is_verified=False).first()
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
