from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from orders.models import OrderCourse


class OrderCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCourse
        fields = (
            'user',
            'ordered',
            'course'
        )

