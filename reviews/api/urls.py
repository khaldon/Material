from django.conf.urls import url
from .views import ReviewDestroyAPIView, ReviewListCreateAPIView

urlpatterns = [
    url(r'^reviews/$', ReviewListCreateAPIView.as_view(), name='list_or_create_reviews'),
    url(r'^reviews/(?P<id>\d+)/$', ReviewDestroyAPIView.as_view(), name='destroy_reviews'),
]