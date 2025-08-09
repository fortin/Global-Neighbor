from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from global_neighbor.views import (
    add_category,
    advanced_search,
    confirm_registration,
    delete_category,
    delete_document,
    document_detail,
    download_document,
    edit_document,
    home,
    library,
    register,
    search,
    upload_document,
    verify_email,
)

app_name = "global_neighbor"

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
    path("search/", search, name="search"),
    path("search/advanced/", advanced_search, name="advanced_search"),
    path("library/", library, name="library"),
    path("library/upload/", upload_document, name="upload_document"),
    path(
        "library/download/<int:document_id>/",
        download_document,
        name="download_document",
    ),
    path("library/document/<int:pk>/", document_detail, name="document_detail"),
    path("library/document/<int:pk>/edit/", edit_document, name="edit_document"),
    path("library/document/<int:pk>/delete/", delete_document, name="delete_document"),
    path("library/categories/add/", add_category, name="add_category"),
    path(
        "library/categories" "/delete/<int:pk>/",
        delete_category,
        name="delete_category",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
