from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Course

class TestCoursesModels(TestCase):
    """
    TestCase class to test the courses models.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.course = Course.objects.create(
            title='test title 1',
            description='some random words'
        )
        # Make `user` the admin & student.
        self.course.admins.add(self.user)
        self.course.students.add(self.user)

        self.other_course = Course.objects.create(
            title='test title 2',
            description='some random words'
        )

    def test_instance_values(self):
        """Test course instance values."""
        self.assertTrue(isinstance(self.course, Course))

    def test_course_return_value(self):
        """Test course string return value."""
        self.assertEqual(str(self.course), 'test title 1')

    def test_courses_list_count(self):
        """Test to count courses."""
        self.assertEqual(Course.objects.count(), 2)

    def test_get_admins_method(self):
        """Test get admins method."""
        self.assertEqual(len(self.course.get_admins()), 1)