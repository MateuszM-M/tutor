from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module


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
        
        
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 
                                              'description',
                                              'order'],
                                              extra=3,
                                              can_delete=True)


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)