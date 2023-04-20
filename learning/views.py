from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView
from users.models import Profile

from .filters import CourseFilter
from .forms import CreateUpdateCourseForm
from .models import Course


class Dashboard(LoginRequiredMixin, TemplateView):
    """
    A class to represent main dashboard view.
    """
    template_name = 'learning/dashboard.html'


class TeacherDashboard(LoginRequiredMixin, FilterView):
    """
    A class to represent teacher dashboard view.
    """
    model = Course
    template_name = 'learning/teacher/teacher_dashboard.html'
    paginate_by = 10
    filterset_class = CourseFilter
    
    def get_queryset(self):
        """
        Returns a list of Courses creasted by request user.
        """
        return Course.objects.filter(owner=self.request.user)


class CreateCourseView(LoginRequiredMixin, CreateView):
    """
    A class to represent create course view.
    """
    model = Course
    form_class = CreateUpdateCourseForm
    template_name = 'learning/teacher/create_course.html'
    success_url = '/teacher/'

    def form_valid(self, form):
        """
        Ovverides the form validation to addtionally assign
        owner of the course to request user and
        slug from slugyfying the course title
        """
        form.instance.owner = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)
    

class CourseDeleteView(DeleteView, LoginRequiredMixin):
    """
    A class to represent delete couse view.
    """
    model = Course
    success_url = '/teacher/'
    template_name = 'learning/teacher/delete_course.html'


class CourseUpdateView(UpdateView, LoginRequiredMixin):
    """
    A class to represent update couse view.
    """
    model = Course
    form_class = CreateUpdateCourseForm
    template_name = 'learning/teacher/update_course.html'
    success_url = '/teacher/'


class CourseDetailView(DetailView, LoginRequiredMixin):
    """
    A class to represent detail course view for user that
    is interested in buying a course.
    """
    model = Course
    template_name = 'learning/student/course_overview.html'

    def get_context_data(self, **kwargs):
        """
        Adds profile to context to make it accessible from templates.
        """
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(
            id=self.object.owner.profile.id)
        return context

