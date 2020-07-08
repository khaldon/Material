from django.contrib import admin
from .models import Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course','reviewer','active','created','updated')
admin.site.register(Review,ReviewAdmin)