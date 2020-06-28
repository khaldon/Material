from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.

class Review(models.Model):
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='posted_reviews', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        """Unicode representation for a comment model."""
        return self.body

    @staticmethod
    def get_reviews(course_slug=None):
        """Returns reviews"""
        if course_slug:
            reviews = Review.objects.filter(active=True,
                                              course__slug__icontains=course_slug)
        else:
            reviews = Review.objects.filter(active=True)
        return reviews

        