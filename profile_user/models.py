from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

