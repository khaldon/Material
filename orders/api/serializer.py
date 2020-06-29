from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from orders import models


#
class OrderCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderCourse
        fields = (
            'user',
            'ordered',
            'course'
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = (
            'user',
            'courses',
            'ordered',
            'ordered_date',
            'payment'
        )

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = (
            'strip_charge_id',
            'user',
            'timestamp'
        )

class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentInfo
        fields = (
            'user',
            'first_name',
            'last_name'
        )
