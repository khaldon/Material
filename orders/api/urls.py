from django.urls import path
from orders.api import views
urlpatterns = [
    path('orders/', views.OrderCourseSerializerList.as_view(), name='orders_list'),
    path('oreder/<id>/', views.OrderCourseSerializerCreate.as_view(), name='order_create')
]
