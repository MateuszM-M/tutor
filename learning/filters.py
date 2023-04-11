import django_filters
from django_filters import CharFilter, DateFilter

from .models import Course


class CourseFilter(django_filters.FilterSet):
    """
    A class to represent filters in view with list of teacher courses.

    Attributes:
    ----------
    title : filtering by title
    created_after : filtering by greater than or equal to created date
    created_before : filtering by lower than or equal to created date
    """
    title = CharFilter(field_name='title', 
                       lookup_expr='icontains',
                       label='Title ')
    created_after = DateFilter(field_name="created", 
                               lookup_expr='gte',
                               label='Created after ')
    created_before = DateFilter(field_name="created", 
                                lookup_expr='lte',
                                label='Created before ')
    
    class Meta:
        model = Course
        fields = ['title']