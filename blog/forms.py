from django import forms
from taggit.forms import TagWidget

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "tags",
        ]
        widgets = {
            "tags": TagWidget(attrs={"placeholder": "Comma-separated tags"}),
        }
