from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Subject(models.Model):
    """
    A class to represent subjects - a course category.
    
    Attributes:
    ----------
    title : title of subject
    slug : slug of subject
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        
    def __str__(self):
        return self.title
    

class Course(models.Model):
    """
    A class to represent courses.

    Attributes:
    -----------

    owner : creator of the course, related to user
    subject : related to subject object
    title : title of the course
    slug : slug of the course, made automatically
    thumbnail : image to represent the course
    overview : basic info about the course
    created : when the course was created
    status : status of the course, to choose from the STATUS_CHOICES
    """

    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )

    owner = models.ForeignKey(get_user_model(),
                              related_name='course_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/')
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES,
                            default='Draft')
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.title
    

class Module(models.Model):
    """
    A class to represent module

    Attributes:
    -----------
    course : course relation
    title : title of the module
    description : description of the module
    """
    course = models.ForeignKey(Course, 
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
    

class Content(models.Model):
    """
    A class to represent content

    Attributes:
    -----------
    module : module relation
    content_type : indicates content type column
    object_id : priamry key of related object
    item : indicates related object based on two abovementioned objects
    """
    module = models.ForeignKey(Module, 
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                      on_delete=models.CASCADE,
                                      limit_choices_to={'model__in':(
                                          'text',
                                          'video',
                                          'image',
                                          'file'
                                          )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    """
    Abstract class to represent different type items

    Attributes:
    -----------
    owner : related user
    title : title of the item
    created : date created
    updated : date updated
    """
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title
    

class Text(ItemBase):
    """
    A class to represent item in type of text

    Attributes:
    -----------
    content : text content of item
    """
    content = models.TextField()
    

class Image(ItemBase):
    """
    A class to represent item in type of image

    Attributes:
    -----------
    image : text content of item
    """
    image = models.FileField(upload_to='images')
    

class Video(ItemBase):
    """
    A class to represent item in type of vido

    Attributes:
    -----------
    video : text content of item
    """
    url = models.URLField()


class File(ItemBase):
    """
    A class to represent item in type of other file

    Attributes:
    -----------
    file : text content of item
    """
    other_file = models.FileField(upload_to='files')