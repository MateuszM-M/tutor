from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .signals import teacher_created

from .models import Profile


class UserLoginForm(AuthenticationForm):
    """
    A class to represent user login form.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructs the login form.
        Uses form helper to render fields as a floating fields
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("password")
        )
        

class RegisterForm(forms.ModelForm):
    """
    A class to represent register form.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructs the register form
        Uses form helper to render register fields as floating fields
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("email"),
            FloatingField("password"),
            FloatingField("password2"),
            HTML(
                '<p>Do you want to create student or teacher account?</p>'
            ),
            Field('is_student'),
            Field('is_teacher')
        )

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    is_student = forms.BooleanField(label='Student',
                                    required=False)
    is_teacher = forms.BooleanField(label='Teacher',
                                    required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        help_texts = {'username': None}

    def clean_password2(self):
        """Checks is passwords are the same"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords must be the same.")
        return cd['password2']
    
    def clean(self):
        """Checks if user chose user role"""
        cd = self.cleaned_data
        if cd['is_student'] == False and cd['is_teacher'] == False:
            raise forms.ValidationError("Choose role")
        return self.cleaned_data
    
    def save(self, commit=True):
        """Overrides save to set password and send signal"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            teacher_created.send(sender='user_created',
                                 is_teacher=self.cleaned_data['is_teacher'],
                                 instance=user)
        return user
    

class ProfileUpdateForm(forms.ModelForm):
    """
    A class to represent profile update form
    """
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location']