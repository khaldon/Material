from orders.api.serializer import  OrderCourseSerializer,  OrderSerializer, PaymentInfoSerializer, PaymentSerializer
from rest_framework.generics import ListCreateAPIView
from orders import models



class OrderCourseSerializerCreate(ListCreateAPIView):
    queryset = models.OrderCourse.objects.all()
    serializer_class = OrderCourseSerializer
    name = 'Order course'


class OrderSerializerCreate(ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = OrderSerializer
    name = 'Order'

class paymentSerializer(ListCreateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = PaymentSerializer
    name = 'Payment'

class PaymentInfoSerializer(ListCreateAPIView):
    queryset = models.PaymentInfo.objects.all()
    serializer_class = PaymentInfoSerializer
    name = 'Payment info'
