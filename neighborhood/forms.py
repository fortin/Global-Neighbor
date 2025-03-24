from django import forms

from .models import ForumCategory, ForumPost, Thread


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ForumCategory
        fields = ["title", "description"]


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "category", "content"]


class PostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["content"]
