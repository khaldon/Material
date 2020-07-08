from django.contrib import admin
from orders.models import OrderCourse, Order
# Register your models here.

class OrderCourseAdmin(admin.ModelAdmin):
    list_display = ('user','ordered','course')
admin.site.register(OrderCourse,OrderCourseAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','ordered','ordered_date')
admin.site.register(Order,OrderAdmin)
