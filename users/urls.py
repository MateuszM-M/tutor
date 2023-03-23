from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm


app_name = 'users'
urlpatterns = [
    path('login/', 
        auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='registration/login.html',
        authentication_form=UserLoginForm),
        name='login'),
    path('logout/', 
        auth_views.LogoutView.as_view(), 
        name='logout'),

    path('register/', 
         views.UserCreateView.as_view(), 
         name='register'),
]