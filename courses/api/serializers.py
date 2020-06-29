from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from courses.models import Course, CourseCategories, CourseSections, SectionVideos
# from accounts.api.serializers import UserDetailSerializer

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = CourseCategories
        fields = ("id", "title")

class CourseSerializer(serializers.ModelSerializer):
    # admins = UserDetailSerializer(read_only=True)
    students_count = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True)
    created_naturaltime = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_wished = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'cover', 'cover_url', 'price', 'category', 'image', 'poster_preview_video', 'preview_video', 'students', 
            'admins', 'students_count', 'created',
            'created_naturaltime', 'is_joined', 'is_admin', 'is_wished',
        ]

    def get_admins(self, obj):
        """Returns a list of admins"""
        return obj.get_admins()

    def get_cover_url(self, obj):
        """Returns course cover url"""
        request = self.context.get('request')
        cover_url = obj.get_picture()
        return request.build_absolute_uri(cover_url)

    def get_students_count(self, obj):
        """Calculates number of students"""
        return obj.students.all().count()
    
    def get_is_joined(self, obj):
        """Checks if user is joined the course"""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.students.all():
            return True
        return False

    def get_is_wished(self, obj):
        """Check if user has wished course"""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.wishes.all():
            return True
        return False

    def get_created_naturaltime(self, obj):
        """Returns human readable time"""
        return naturaltime(obj.created)

    def get_is_admin(self, obj):
        """Checks if user is admin"""
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user in obj.admins.all():
            return True
        return False

    def create(self, validated_data):
        """Handles the creation of course"""
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        instance.admins.add(user)
        instance.save()
        return instance

class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSections
        fields = ['creator', 'title', 'course']

    def create(self, validated_data):
        """Handles the creation of course section"""
        instance = self.Meta.model(**validated_data)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        instance.save()
        instance.creator.add(user)
        instance.save()
        return instance

class SectionVideoSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    created_naturaltime = serializers.SerializerMethodField()

    class Meta:
        model = SectionVideos
        fields = ['title', 'video', 'section', 'preview_image', 'short_description', 'watched', 'created']

    def get_created_naturaltime(self, obj):
        """Returns human readable time"""
        return naturaltime(obj.created)

    def get_preview_image_url(self, obj):
        """Returns section video's preview image url"""
        request = self.context.get('request')
        preview_image_url = obj.get_picture()
        return request.build_absolute_uri(preview_image_url)