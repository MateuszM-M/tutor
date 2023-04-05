from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, TemplateView
from .forms import CreateCourseForm

from .models import Course


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'learning/dashboard.html'


class TeacherDashboard(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'learning/teacher/teacher_dashboard.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)
    

class CreateCourse(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'learning/teacher/create_course.html'
    success_url = '/teacher/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)