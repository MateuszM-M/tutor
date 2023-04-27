from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView
from users.models import Profile

from .filters import CourseFilter
from .forms import CreateUpdateCourseForm
from .models import Course


class OwnerMixin(object):
    """
    A mixin that overrides the queryset to filter objects by request user
    """
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin(object):
    """
    A mixin for creation and update, 
    which assings course owner to request user
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    """
    A mixin that assing model to course
    """
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    A mixin that assings form and succes_url
    """
    form_class = CreateUpdateCourseForm
    success_url = reverse_lazy('learning:teacher_dashboard')


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    A class to represent main dashboard view.
    """
    template_name = 'learning/dashboard.html'


class TeacherDashboard(OwnerCourseMixin, FilterView):
    """
    A class to represent teacher dashboard view.
    """
    template_name = 'learning/teacher/teacher_dashboard.html'
    paginate_by = 10
    filterset_class = CourseFilter
        

class CourseCreateView(PermissionRequiredMixin, 
                       OwnerCourseEditMixin,
                       CreateView):
    """
    A class to represent create course view.
    """
    template_name = 'learning/teacher/create_course.html'
    success_url = '/teacher/'
    permission_required = 'learning.add_course'

    def form_valid(self, form):
        """
        Overides the form validation to addtionally assign
        slug from slugyfying the course title
        """
        form.instance.slug = slugify(form.instance.title)
        return super(CourseCreateView, self).form_valid(form)
    

class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin, 
                       DeleteView):
    """
    A class to represent delete couse view.
    """
    success_url = '/teacher/'
    template_name = 'learning/teacher/delete_course.html'
    permission_required = 'learning.delete_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    """
    A class to represent update couse view.
    """
    template_name = 'learning/teacher/update_course.html'
    success_url = '/teacher/'
    permission_required = 'learning.change_course'


class CourseDetailView(OwnerCourseMixin, DetailView):
    """
    A class to represent detail course view for user that
    is interested in buying a course.
    """
    template_name = 'learning/student/course_overview.html'

    def get_context_data(self, **kwargs):
        """
        Adds profile to context to make it accessible from templates.
        """
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(
            id=self.object.owner.profile.id)
        return context


class LearningView(DetailView, LoginRequiredMixin):
    """
    A class to represent learning view for user that bought course.
    """
    model = Course
    template_name = 'learning/student/learning_view.html'