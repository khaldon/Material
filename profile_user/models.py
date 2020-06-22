from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class ProfileUser(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    birth_date = models.DateField()
    image = models.ImageField(upload_to='user_images', null=True, blank=True)

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/default_picture.png'
        if self.image:
            return self.image.url
        else:
            return default_picture

    def __str__(self):
        return self.user
