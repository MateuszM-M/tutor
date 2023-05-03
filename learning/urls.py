from django.urls import path

from . import views

app_name = "learning"
urlpatterns = [
    path('dashboard/', 
         views.Dashboard.as_view(),
           name='dashboard'),
    path('teacher/', 
         views.TeacherDashboard.as_view(),
           name='teacher_dashboard'),

    path('teacher/create_course', 
         views.CourseCreateView.as_view(), 
         name='create_course'),

    path('teacher/delete_course/<str:slug>', 
         views.CourseDeleteView.as_view(), 
         name='delete_course'),    

    path('teacher/update_course/<str:slug>', 
         views.CourseUpdateView.as_view(), 
         name='update_course'),

     path('course/overview/<str:slug>/',
          views.CourseDetailView.as_view(),
          name='detail_course'),

     path('course/learning/<str:slug>/',
          views.LearningView.as_view(),
          name='learning_view'),

     path('course/formset/<str:pk>/',
          views.CourseModuleUpdateView.as_view(),
          name='course_module_update'),

     path('module/<int:module_id>/content/<model_name>/create',
          views.ContentCreateUpdateView.as_view(),
          name='module_content_create'),

     path('module/<int:module_id>/content/<module_name>/<id>',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),

     path('content/<int:id>/delete',
          views.ContentDeleteView.as_view(),
          name='module_content_delete'),
]