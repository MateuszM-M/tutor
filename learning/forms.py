from django import forms
from .models import Course


class CreateUpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'subject', 
            'title', 
            'overview', 
            'thumbnail', 
            'status',
            ]