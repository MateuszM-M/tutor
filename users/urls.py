from django.contrib.auth import views as auth_views
from django.urls import path


app_name = 'users'
urlpatterns = [
    path('login/', 
        auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='registration/login.html'),
        name='login'),
]