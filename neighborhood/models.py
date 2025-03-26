from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from models_extensions.models import ActivatorModel, TimeStampedModel
from taggit.managers import TaggableManager

User = get_user_model()


class ForumCategory(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Thread(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        ForumCategory, on_delete=models.CASCADE, related_name="threads"
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="threads"
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ForumPost(TimeStampedModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    content = models.TextField()
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"Post by {self.author} on {self.created}"
