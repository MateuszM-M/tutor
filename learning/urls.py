from django.urls import path

from . import views

app_name = "learning"
urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('teacher/', views.TeacherDashboard.as_view(), name='teacher_dashboard'),
]