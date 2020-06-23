from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',views.UserLoginAPIView.as_view(),name='login'),
    url(r'^signup/$',views.UserSignUpAPIView.as_view(),name='signup'),
]