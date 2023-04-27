import os
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.utils.text import slugify
from PIL import Image


class User(AbstractUser):
    """
    DB model to alter built-in Django User model in future
    """
    pass


class Profile(models.Model):
    """
    DB model to extend User model with attributes that are not mandatory.

    Attributes:
    -----------
    user : user object related to profile
    profile_picture : profile picture
    bio : information about user
    location : user location
    """
    user = models.OneToOneField(get_user_model(),
                             on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default="profile_pictures/profile_default.jpg",
        blank=True, 
        null=True,
        upload_to='profile_pictures/')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    def restore_default_picutre(self, *args, **kwargs):
        """
        Restores default profile picture on delete
        """
        if self.profile_picture:
            pass
        else:
            self.profile_picture = 'profile_pictures/profile_default.jpg'
        return self.profile_picture
    
    def resize(self, *args, **kwargs):
        """
        Resizes the profile picture on save
        """
        img = Image.open(self.profile_picture)
        file_format = img.format
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200), Image.ANTIALIAS)
            img_io = BytesIO()
            img.save(img_io, file_format)
            img_io.seek(0)
            suf = SimpleUploadedFile(
                os.path.split(self.profile_picture.name)[-1],
                  img_io.read())
            self.profile_picture.save(suf.name + file_format, suf, save=False)
        return self.profile_picture
    
    def add_slug(self, *args, **kwargs):
        """
        Adds slug to profile.
        """
        self.slug = slugify(self.user.get_username())
        return self.slug


    def save(self, *args, **kwargs):
        """
        Overrise save to add additional methods
        """
        self.profile_picture = self.restore_default_picutre()
        self.profile_picture = self.resize()
        self.slug = self.add_slug()
        super(Profile, self).save(*args, **kwargs)

