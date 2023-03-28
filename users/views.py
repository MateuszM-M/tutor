from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    success_message = "Your account has been created successfully"

    
class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = Profile


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = Profile
    template_name = 'users/edit_profile.html'
    form_class = ProfileUpdateForm
    success_message = "Your profile has been updated successfully"
    
    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': profile_id})
    

class DefaultLogIn(RedirectView, SuccessMessageMixin):
    url = reverse_lazy('learning:dashboard')

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        user = User.objects.get(id=2)

        if user is not None:
            login(request, user)
            messages.add_message(
                request, 
                messages.SUCCESS, 
                'You have been automatically logged in')
            return redirect('learning:dashboard')
        

class Custom400View(TemplateView):
    template_name = "errors/400.html"


class Custom403View(TemplateView):
    template_name = "errors/403.html"


class Custom404View(TemplateView):
    template_name = "errors/404.html"


class Custom500View(TemplateView):
    template_name = "errors/500.html"

