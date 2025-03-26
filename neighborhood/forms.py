from django import forms
from taggit.forms import TagWidget

from .models import ForumCategory, ForumPost, Thread


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ForumCategory
        fields = ["title", "description"]


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "category"]


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["content", "tags"]  # ✅ Only valid ForumPost fields
        widgets = {
            "tags": TagWidget(attrs={"placeholder": "Add tags separated by commas"}),
        }
