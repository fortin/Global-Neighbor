from django import forms
from taggit.forms import TagWidget

from .models import BlogComment, BlogPost


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


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write a comment..."}
            )
        }
