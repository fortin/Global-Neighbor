from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from models_extensions.models import ActivatorModel, TimeStampedModel
from taggit.managers import TaggableManager

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
    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
