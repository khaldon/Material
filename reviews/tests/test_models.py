from django.contrib.auth import get_user_model
from django.test import TestCase
from courses.models import Course
from ..models import Review

class TestCommentsModels(TestCase):
    """
    TestCase class to test the reviews models
    """
    def setUp(self):
        self.user = get_user_model().objects.create(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.course = Course.objects.create(
            title='test title',
            description='some random words'
        )
        self.review = Review.objects.create(
            body='some random words',
            reviewer=self.user,
            course=self.course
        )

    def test_instance_values(self):
        self.assertTrue(isinstance(self.review, Review))

    def test_review_return_value(self):
        self.assertEqual(str(self.review), 'some random words')

    def test_review_list_count(self):
        """Test to count comments"""
        self.assertEqual(Review.objects.count(), 1)