from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, CourseCategories, CourseSections, SectionVideos
from .permissions import IsAdminOrReadOnly
from .serializers import CourseSerializer, CategorySerializer, CourseSectionSerializer, SectionVideoSerializer
from rest_framework import filters
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

class CategoryListAPIView(ListAPIView):
    queryset = CourseCategories.objects.all()
    serializer_class = CategorySerializer

class CourseFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    class Meta:
        model = Course
        fields = ['min_price', 'max_price']

class CourseListCreateAPIView(ListCreateAPIView):
    """
    View that returns a list of courses & handles the creation of
    courses & returns data back
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title','description','price','category__title']
    filter_class = CourseFilter

class CourseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    View that retrieve, update or delete (if user is the admin of) the course
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

class JoinCourseView(APIView):
    
    def get(self, request, format=None):
        """
        View that join a course and returns action status
        """
        data = dict()
        user = request.user
        course_slug = request.GET.get('course_slug')
        course = Course.objects.get(slug=course_slug)
        user = request.user
        if course in user.joined_courses.all():
            pass
        else:
            course.students.add(user)
            data['is_joined'] = True
        data['total_students'] = course.students.count()
        return Response(data)

class GetJoinedCourses(APIView):
    def get(self, request, format=None):
        """Return a list of user joined courses"""
        courses = request.user.joined_courses.all()
        courses_list = [{'id': course.id, 'title': course.title} for course in courses]
        return Response(courses_list)

class WishCourseView(APIView):
    def get(self, request, format=None):
        """
        View that wish a course and returns action status
        """
        data = dict()
        user = request.user
        course_slug = request.GET.get('course_slug')
        course = Course.objects.get(slug=course_slug)
        user = request.user
        if course in user.wished_courses.all():
            course.wishes.remove(user)
            data['is_wished'] = False
        else:
            course.wishes.add(user)
            data['is_wished'] = True
        data['total_wishes'] = course.wishes.count()
        return Response(data)

class GetWishedCourses(APIView):
    def get(self, request, format=None):
        """Return a list of user wished courses"""
        courses = request.user.wished_courses.all()
        courses_list = [{'id': course.id, 'title': course.title} for course in courses]
        return Response(courses_list)

class SectionsListCreateAPIView(ListCreateAPIView):
    """
    View that returns a list of sections & handles the creation of
    sections & returns data back
    """
    queryset = CourseSections.objects.all()
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']

# class SectionsListCreateAPIView(ListCreateAPIView):
#     """
#     View that returns a list of sections & handles the creation of
#     sections & returns data back
#     """
#     queryset = CourseSections.objects.all()
#     serializer_class = CourseSectionSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ['title']

class SectionsListAPIView(RetrieveAPIView):
    """
    View that returns a list of sections & handles the creation of
    sections & returns data back
    """
    queryset = CourseSections.objects.all()
    lookup_field = "course__slug"
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SectionsCreateAPIView(CreateAPIView):
    queryset = CourseSections.objects.all()
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'course__slug'

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)