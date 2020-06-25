from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import UniqueSlugify
from django.urls import reverse
# from languages.fields import LanguageField

# Create your models here.

User = settings.AUTH_USER_MODEL

class CourseCategories(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/course_images',blank=True,null=True , default='courses/image.png')
    cover = models.ImageField(upload_to='courses/course_covers',blank=True,null=True)
    admins = models.ManyToManyField(User, related_name='creator')
    students = models.ForeignKey(User,related_name='joined_courses',blank=True,null=True,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CourseCategories,on_delete=models.CASCADE)
    certificate = models.ImageField(upload_to='courses/course_certificates',blank=True,null=True)
    rank_score = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    discount_price = models.FloatField(blank=True, null=True)
    preview_video = models.FileField(upload_to='courses/course_preview_videos',max_length=100,null=True)
    poster_preview_video = models.ImageField(upload_to='courses/course_poster_preview', null=True)    
    owned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = course_slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_admins(self):
        """Return admins of a course."""
        return self.admins.all()

    def get_picture(self):
        """Return cover url (if any) of a course."""
        default_picture = settings.STATIC_URL + 'img/cover.png'
        if self.cover:
            return self.cover.url
        else:
            return default_picture

    def __str__(self):
        return self.title

class CourseSections(models.Model):
    creator = models.ForeignKey(User,related_name='creator_sections',on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, related_name='course_section', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

class SectionVideos(models.Model):
    title = models.CharField(max_length=50,null=True)
    video = models.FileField(upload_to='courses/course_videos',max_length=100)
    section = models.ForeignKey(CourseSections,on_delete=models.CASCADE,null=True)
    preview_image = models.ImageField(upload_to='courses/course_videos_preview_images',null=True)
    short_description = models.CharField(max_length=50,null=True)
    watched = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def get_absolute_url(self):
        return reverse('courses:course_detail',args=[self.section.course.slug])

@receiver(post_save, sender=Course)
def create_section_course(sender, instance, created, **kwargs):
    if created:
        CourseSections.objects.create(course=instance)

@receiver(post_save, sender=Course)
def save_section_course(sender, instance, **kwargs):
    instance.course_section.save()

course_slugify = UniqueSlugify(
                    to_lower=True,
                    max_length=80,
                    separator='_',
                    capitalize=False
                )
