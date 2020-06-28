from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Review
from .permissions import IsReviewerOrReadOnly
from .serializers import ReviewSerializer

class ReviewListCreateAPIView(ListCreateAPIView):
    """
    View that returns reivews list of a single course & handles the creation
    of reviews & returns data back
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        course_slug = self.request.GET.get('course_slug', '')
        queryset_list = Review.get_reviews(course_slug)
        return queryset_list

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class ReviewDestroyAPIView(DestroyAPIView):
    """
    View that delete the reivew
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    