from django.contrib import admin
from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    A class to represent a Subject in admin panel.

    Attributes:
    ----------
    list_display : displays title and slug of the subject
    prepopulated_fields : autmatically populate slug field
    """
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    """
    A class to represent a inlined Module in Course in admin panel.
    """
    model = Module

    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    A class to represent Course in admin panel.

    Attributes:
    -----------
    list_display : defines course attributes displayed in list view
    list_filter : allows filtering by created date and subject
    search_fields : allows searching by title and overvie
    prepopulated_fields : autmatically populate slug field
    inlines : inlined Module class
    """
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
