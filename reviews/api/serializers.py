from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from reviews.models import Review
from accounts.api.serializers import UserDetailSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer that represents a comment.
    """
    reviewer = UserDetailSerializer(read_only=True)
    is_reviewer = serializers.SerializerMethodField()
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'body', 'course', 'reviewer', 'is_reviewer',
            'created', 'created_naturaltime',
        ]

    def get_is_reviewer(self, obj):
        """Checks if user is the reviewer"""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user == obj.reviewer:
            return True
        return False

    def get_created_naturaltime(self, obj):
        """Returns human readable time"""
        return naturaltime(obj.created)

    def create(self, validated_data):
        """Handles the creation of review"""
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        return instance

        