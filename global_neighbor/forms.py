from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Document, User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Prevent login until email verification
        if commit:
            user.save()
        return user


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "author", "source", "category", "tags", "file"]
        widgets = {
            "tags": forms.TextInput(attrs={"placeholder": "Comma-separated tags"}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "author", "source", "category", "tags"]
