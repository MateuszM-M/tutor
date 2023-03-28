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

    path('profile/<str:pk>/',
         views.ProfileView.as_view(),
         name='profile'),

    path('profile-edit/<str:pk>',
         views.ProfileUpdateView.as_view(),
         name='profile_edit'), 

    path('',
          views.DefaultLogIn.as_view(),
          name='default_log_in'),
]