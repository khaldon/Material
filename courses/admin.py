from django.contrib import admin
from .models import Course, CourseCategories, CourseSections, SectionVideos, Rating

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated', 'price', 'cover', 'preview_video')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'created'
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseCategories)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'course',)
admin.site.register(CourseSections,SectionAdmin)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('section', 'title', 'created', 'video')
    date_hierarchy = 'created'
admin.site.register(SectionVideos,VideoAdmin)
admin.site.register(Rating)
