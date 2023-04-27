from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileInline(admin.StackedInline):
    """
    A class to represent inlined Profile in User in admin panel.
    """
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    A class to represent User in admin panel.

    Attributes:
    -----------
    list_display : defines user attributes displayed in list view
    inlines : inlined Module class
    """
    list_display = ['username', 'email', 'date_joined']
    inlines = [ProfileInline]

