from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.

class Notification(models.Model):
    """
    Model that represents a notification
    """
    NOTIF_CHOICES = (
        ('review', 'Review on Course'),
        ('follow', 'Followed by someone'),
        ('sent_msg_request', 'Sent a Message Request'),
        ('confirmed_msg_request', 'Sent a Message Request'),
    )

    Actor = models.ForeignKey(User, related_name='c_acts', on_delete=models.CASCADE)
    Object = models.ForeignKey(Course, related_name='act_notif', null=True, blank=True, on_delete=models.SET_NULL)
    Target = models.ForeignKey(User, related_name='c_notif', on_delete=models.CASCADE)
    notif_type = models.CharField(
        max_length=500, choices=NOTIF_CHOICES, default='Review on Course'
    )
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        """
        Unicode representation for a notification based on notification type
        """
        if self.notif_type == 'review':
            return '{} reviewed your course \"{}\".'.format(
                self.Actor.profile.screen_name(), self.Object
            )
        elif self.notif_type == 'follow':
            return '{} followed you.'.format(
                self.Actor.profile.screen_name()
            )
        elif self.notif_type == 'sent_msg_request':
            return '{} sent you a message request.'.format(
                self.Actor.profile.screen_name()
            )
        else:
            return '{} accepted your message request.'.format(
                self.Actor.profile.screen_name()
            )

    @staticmethod
    def get_user_notification(user):
        """Returns user notifications"""
        if user:
            notifications = Notification.objects.filter(Target=user).exclude(Actor=user)
            return notifications
        return []