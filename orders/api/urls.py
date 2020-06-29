from django.urls import path
from orders.api import views
urlpatterns = [
    path('order_course/', views.OrderCourseSerializerCreate.as_view(), name='order_course'),
    path('order/', views.OrderSerializerCreate.as_view(), name='order'),
    path('payment/', views.paymentSerializer.as_view(), name='payment'),
    path('payment/info/', views.PaymentInfoSerializer.as_view(), name='payment')
]
