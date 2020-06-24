from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title','description','category','image','cover','languages','price','preview_video','poster_preview_video')