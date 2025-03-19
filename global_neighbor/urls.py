from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from global_neighbor.views import confirm_registration, home, register, verify_email

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls", namespace="blog")),
    path("forum/", include("neighborhood.urls", namespace="neighborhood")),
    # Authentication URLs
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", register, name="register"),
    path("confirm-registration/", confirm_registration, name="confirm_registration"),
    path("verify/<uuid:token>/", verify_email, name="verify_email"),
]
