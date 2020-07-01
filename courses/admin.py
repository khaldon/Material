from django.contrib import admin
from .models import Course, CourseCategories, CourseSections, SectionVideos

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseCategories)
admin.site.register(CourseSections)
admin.site.register(SectionVideos)
admin.site.register(Rating)
