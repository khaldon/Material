from django.urls import path
from . import views
from rest_framework import routers

# router.register('profile/<pk>', )

urlpatterns = [
    path('profile/', views.ProfileUserList.as_view(), name=views.ProfileUserList.name),
    path('profile/<pk>/', views.ProfileUserDetail.as_view(), name='')
]
