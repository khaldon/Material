from django.urls import path
from orders.api import views
urlpatterns = [
    path('create/', views.OrderCourseSerializerCreate.as_view(), name='order_create')
]
