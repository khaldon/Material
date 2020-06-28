from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import OrderCourse
from courses.models import Course


class TestOrderCourse(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test1',
            email='test@gmail.com',
            password='helloworld',
        )
        self.course = Course.objects.get(id=7)
        self.order_course = OrderCourse.objects.create(user=self.user,
                                                       ordered=True,
                                                       course=self.course)



    def test_course_return_value(self):
        """Test to count courses."""
        self.assertEqual(str(self.order_course), 'test title 1')

