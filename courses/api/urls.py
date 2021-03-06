from django.conf.urls import url
from .views import (CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView,
                    GetJoinedCourses, JoinCourseView, WishCourseView,
                    GetWishedCourses, CategoryListAPIView, SectionsListAPIView,
                    SectionsCreateAPIView, VideosListAPIView,CartView,AddCart,
                    VideosCreateAPIView, RatingListAPIView, RatingCreateAPIView)

urlpatterns = [

    url(r'^courses/$', CourseListCreateAPIView.as_view(), name='list_or_create_courses'),
    url(r'^courses/(?P<slug>[-\w]+)/$',CourseRetrieveUpdateDestroyAPIView.as_view(),name='retrieve_or_update_or_destroy_courses'),
    url(r'^actions/join/$', JoinCourseView.as_view()),
    url(r'^videos/create/$', VideosCreateAPIView.as_view(), name='create_videos'),
    url(r'^user_joined_courses/$', GetJoinedCourses.as_view()),
    url(r'^actions/wish/$', WishCourseView.as_view()),
    url(r'^user_wished_courses/$', GetWishedCourses.as_view()),
    url(r'^categories/$', CategoryListAPIView.as_view(), name='list_categories'),
    url(r'^sections/(?P<course__slug>[-\w]+)/$', SectionsListAPIView.as_view(), name='list_sections'),
    url(r'^sections/(?P<course__slug>[-\w]+)/create/$', SectionsCreateAPIView.as_view(), name='create_sections'),
    url(r'^videos/(?P<section__title>[-\w]+)/$', VideosListAPIView.as_view(), name='list_videos'),
    url(r'^rates/(?P<course__slug>[-\w]+)/$', RatingListAPIView.as_view(), name='list_rates'),
    url(r'^rate/create/(?P<course>.+)/$', RatingCreateAPIView.as_view(), name='rate'),
    url(r'^cart/$', CartView.as_view(), name='cart_view'),
    url(r'cart/add/(?P<pk>.+)/', AddCart.as_view(), name='add_cart')
]
