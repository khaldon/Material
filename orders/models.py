from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
# Create your models here.



class OrderCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def get_total_discount_course_price(self):
        return self.course.discount_price

    def get_total_course_price(self):
        return self.course.price

    def get_final_price(self):
        if self.course.discount_price:
            return self.get_total_discount_course_price()
        return self.get_total_course_price()

    def get_amount_saved(self):
        return self.get_total_course_price() - self.get_total_discount_course_price()

    def __str__(self):
        return self.course.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(OrderCourse)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_course in self.courses.all():
            total += order_course.get_final_price()
        return total

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=70)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class PaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default=False)
    last_name = models.CharField(max_length=100, default=False)

    def __str__(self):
        return '{} {} {}'.format(self.user.username, self.first_name, self.last_name)


