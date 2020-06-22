from django.conf.urls import url
from .views import UserLoginAPIView, UserSignUpAPIView

urlpatterns = [
    url(r'^login/', UserLoginAPIView.as_view(), name='users_login'),
    url(r'^signup/', UserSignUpAPIView.as_view(), name='users_signup'),
]