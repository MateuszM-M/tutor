from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from .models import Course, Module


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'learning/dashboard.html'


class TeacherDashboard(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'learning/teacher/teacher_dashboard.html'
    
    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)