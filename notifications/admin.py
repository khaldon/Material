from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('Actor','Object','Target','notif_type','is_read','created')
admin.site.register(Notification,NotificationAdmin)