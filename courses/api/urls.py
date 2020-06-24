from django.conf.urls import url
from .views import CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView, GetJoinedCourses, JoinCourseView

urlpatterns = [
    url(r'^courses/$', CourseListCreateAPIView.as_view(), name='list_or_create_courses'),
    url(r'^courses/(?P<slug>[-\w]+)/$',CourseRetrieveUpdateDestroyAPIView.as_view(),name='retrieve_or_update_or_destroy_courses'),
    url(r'^actions/join/$', JoinCourseView.as_view()),
    url(r'^user_joined_courses/$', GetJoinedCourses.as_view()),
]