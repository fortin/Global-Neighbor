from rest_framework import serializers

from .models import BlogCategory, BlogPost


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    categories = BlogCategorySerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = "__all__"
