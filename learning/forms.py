from django import forms
from .models import Course


class CreateUpdateCourseForm(forms.ModelForm):
    """
    A class to represent create and update form for a Course.
    """
    class Meta:
        model = Course
        fields = [
            'subject', 
            'title', 
            'overview', 
            'thumbnail', 
            'status',
            ]