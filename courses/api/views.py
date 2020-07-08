from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, CourseCategories, CourseSections, SectionVideos, Rating
from orders.models import OrderCourse, Order
from orders.api.serializer import CartSerializer
from .permissions import IsAdminOrReadOnly
from .serializers import (CourseSerializer, CategorySerializer, CourseSectionSerializer,
                          SectionVideoSerializer, RatingSerializer)
from rest_framework import filters
from django.utils import timezone
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.shortcuts import get_object_or_404

def check_video_extension(filename):
    """Checks filename extension"""
    ext = ['.mp4', '.webm', '.mkv', '.avi', '.wmv', '.amv', '.m4v', 'flv', 'flv' ]
    for e in ext:
        if filename.endswith(e):
            return True
    return False

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

class SectionsListAPIView(ListAPIView):
    """
    View that returns a list of sections & handles the creation of
    sections & returns data back
    """
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = serializer_class.Meta.model
    lookup_field = 'course__slug'

    def get_queryset(self):
        course__slug = self.kwargs["course__slug"]
        queryset = self.model.objects.filter(course__slug=course__slug)
        return queryset

class SectionsCreateAPIView(CreateAPIView):
    queryset = CourseSections.objects.all()
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'
    lookup_url_kwarg = 'course__slug'

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs.get('course__slug'))
        if serializer.is_valid():
            serializer.save(creator=self.request.user,course=course)
        else:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)

class RatingListAPIView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = serializer_class.Meta.model
    lookup_field = 'course__slug'

    def get_queryset(self):
        course__slug = self.kwargs["course__slug"]
        queryset = self.model.objects.filter(course__slug=course__slug)
        return queryset

class RatingCreateAPIView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, course):
        course  = Course.objects.get(slug=course)
        rating = self.request.query_params.get('rate')
        student = request.user.id
        context = {'course': course.id, 'student': student, 'rating': rating}
        serializer = RatingSerializer(data=context)
        if course.course_rate.all().filter(student=request.user).count() == 0:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Rating is onetime only", status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    def get(self, *args,  **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return Response(order)
        except ObjectDoesNotExist:
            return Response("Doesn't exits")

class AddCart(ListCreateAPIView):
    queryset = OrderCourse.objects.all()
    serializer_class = CartSerializer
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        order_course, created = OrderCourse.objects.get_or_create(
        course=course,
        user=request.user,
        ordered = False,
    )
        order_qs = Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.courses.filter(course__pk=course.pk).exists():
                return Response("You already have this course in the cart")
            else:
                order.courses.add(order_course)
                return Response("This course was added to your cart.")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        return Response("You already have this course in the cart")

class VideosListAPIView(ListAPIView):
    """
    View that returns a list of videos & handles the creation of
    videos & returns data back
    """

    lookup_field = "section__title"
    serializer_class = SectionVideoSerializer
    model = serializer_class.Meta.model
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        section__title = self.kwargs["section__title"]
        queryset = self.model.objects.filter(section__title=section__title)
        return queryset

class VideosCreateAPIView(ListCreateAPIView):
    queryset = SectionVideos.objects.all()
    serializer_class = SectionVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
