from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from models_extensions.models import ActivatorModel, TimeStampedModel
from taggit.managers import TaggableManager

from global_neighbor.scripts.utils import generate_unique_slug

User = get_user_model()


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="blog_posts"
    )
    content = models.TextField()
    categories = models.ManyToManyField(BlogCategory, blank=True, related_name="posts")
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(BlogPost, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(
        "BlogPost", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_blog_comments", blank=True
    )

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

    def is_reply(self):
        return self.parent is not None
