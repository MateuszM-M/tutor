from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Profile

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_teacher', 'is_student', 
                    'date_joined']
    inlines = [ProfileInline]

    
admin.site.unregister(Group)