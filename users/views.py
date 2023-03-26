from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    success_message = "Your profile was created successfully"

    
class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'users/edit_profile.html'
    form_class = ProfileUpdateForm
    
    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': profile_id})