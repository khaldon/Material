from django.urls import path
from . import views
from rest_framework import routers

# router.register('profile/<pk>', )

urlpatterns = [
    path('users/', views.ProfileList.as_view(), name=views.ProfileList.name),
    # path('<pk>/', views.ProfileUserDetail.as_view(), name='')
]
