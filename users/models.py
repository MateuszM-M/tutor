from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    DB model to alter built-in Django User model.
    
    Attributes
    ----------
    is_student : if True, student features access gained
    is_teacher : if True, teacher features access gained
    """
    is_student = models.BooleanField('student', default=False)
    is_teacher = models.BooleanField('teacher', default=False)


class Profile(models.Model):
    """
    DB model to extend User model with attributes that are not mandatory.
    """
    user = models.OneToOneField(get_user_model(),
                             on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default="profile_default.jpg",
        blank=True, 
        null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        """
        Restores default 
        """
        if self.profile_picture:
            pass
        else:
            self.profile_picture = 'profile_default.jpg'
        super().save(*args, **kwargs)

