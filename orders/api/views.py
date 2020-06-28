from orders.api.serializer import OrderCourseSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from orders.models import OrderCourse


class OrderCourseSerializerCreate(ListCreateAPIView):
    queryset = OrderCourse.objects.all()
    serializer_class = OrderCourseSerializer
    name = 'Create order'

