from django import dispatch
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Profile

user = get_user_model()

@receiver(post_save, sender=user)
def create_profile(sender, instance, created, **kwargs):
	"""
	Creates profile after user creation
	"""
	if created:
		Profile.objects.create(user=instance)


user_created = dispatch.Signal()


@receiver(user_created)
def add_to_teacher_group(sender, 
			 instance, 
			 is_student, 
			 is_teacher, 
			 **kwargs):
	"""
	Adds to the group Teachers if teacher boolean field
	filled on registration.
	"""
	if is_student:
		my_group = Group.objects.get(name='Students') 
		my_group.user_set.add(instance)
	if is_teacher:
		my_group = Group.objects.get(name='Teachers') 
		my_group.user_set.add(instance)
