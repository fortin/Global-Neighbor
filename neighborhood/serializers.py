from rest_framework import serializers

from .models import ForumCategory, ForumPost, Thread


class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = "__all__"


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = "__all__"
