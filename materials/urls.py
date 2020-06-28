"""materials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/profile/', include('profile_user.api.urls')),
    re_path(r'^api/accounts/', include('accounts.api.urls')),
    re_path(r'^api/courses/', include('courses.api.urls')),
<<<<<<< HEAD
    re_path(r'^api/order/', include('orders.api.urls')),
=======
    re_path(r'^api/reviews/', include('reviews.api.urls')),
>>>>>>> fa211371097864b840d16422eff3e7fbfdc739d0
    re_path(r'^api/auth/token/obtain/', obtain_jwt_token),
    re_path(r'^api/auth/token/refresh/', refresh_jwt_token),
    re_path(r'^api/auth/token/verify/', verify_jwt_token),

]
