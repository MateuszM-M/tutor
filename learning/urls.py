from django.urls import path

from . import views

app_name = "learning"
urlpatterns = [
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('teacher/', views.TeacherDashboard.as_view(), name='teacher_dashboard'),
    path('teacher/create_course', views.CreateCourse.as_view(), name='create_course'),
]