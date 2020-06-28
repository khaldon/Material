from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from orders.models import OrderCourse


class OrderCourseSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    course = serializers.HyperlinkedRelatedField(view_name='course_detail', read_only=True)

    class Meta:
        model = OrderCourse
        fields = (
            'user',
            'ordered',
            'course'
        )

