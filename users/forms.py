from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("password")
        )
        

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
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

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'is_student', 'is_teacher')
        help_texts = {'username': None}

    def clean_password2(self):
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
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user