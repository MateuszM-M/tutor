from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProfileUpdateForm, RegisterForm
from .models import Profile


class UserCreateView(SuccessMessageMixin, CreateView):
    """A class to represent user creation view """
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('learning:dashboard')
    success_message = "%(username)s, your account has been created successfully"

    def login_after_register(self):
        """
        Logs in user after registration.
        """
        login(self.request, self.object)
        
    def form_valid(self, form):
        """
        Override form_valid method to use method login after register
        """
        valid = super(UserCreateView, self).form_valid(form)

        self.login_after_register()

        return valid

    
class ProfileView(DetailView):
    """
    A class to represent profile information view
    """
    template_name = 'users/profile.html'
    model = Profile


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    """
    A class to represent user update view.
    """
    model = Profile
    template_name = 'users/edit_profile.html'
    form_class = ProfileUpdateForm
    success_message = "Your profile has been updated successfully"
    
    def get_success_url(self):
        """
        Gets user pk to use in URL.
        """
        profile_id = self.kwargs['pk']
        return reverse_lazy('users:profile', kwargs={'pk': profile_id})
    

class DefaultLogIn(RedirectView, SuccessMessageMixin):
    """
    A class that is used to automatically log in a user
    """
    url = reverse_lazy('learning:dashboard')

    def get(self, request, *args, **kwargs):
        """
        Logs as user with id 2 on GET on main site.
        User with id 2 should always be provided in fixture.
        """
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
    """
    A class to handle 400 error
    """
    template_name = "errors/400.html"


class Custom403View(TemplateView):
    """
    A class to handle 403 error
    """
    template_name = "errors/403.html"


class Custom404View(TemplateView):
    """
    A class to handle 404 error
    """
    template_name = "errors/404.html"


class Custom500View(TemplateView):
    """
    A class to handle 500 error
    """
    template_name = "errors/500.html"
