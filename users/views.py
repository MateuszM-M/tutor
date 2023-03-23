from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegisterForm


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    success_message = "Your profile was created successfully"