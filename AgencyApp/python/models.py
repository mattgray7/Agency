from __future__ import unicode_literals

import json
from django.db import models
from django.core.files.storage import FileSystemStorage

from django.conf import settings
imageStorage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}/'.format(settings.MEDIA_URL),
)

def image_directory_path(instance, filename):
    if hasattr(instance, "username"):
        inputString = instance.username
    elif (isinstance(instance, EventPost) or 
          isinstance(instance, ProjectPost) or
          isinstance(instance, WorkPost) or
          isinstance(instance, CollaborationPost) or
          isinstance(instance, CastingPost) and
          hasattr(instance, "poster")):
        inputString = instance.poster
    return u'{0}/{1}'.format(inputString, filename)

# Create your models here.
class UserAccount(models.Model):
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    setupComplete = models.BooleanField(default=False)
    workInterest = models.BooleanField(default=False)
    crewInterest = models.BooleanField(default=False)
    collaborationInterest = models.BooleanField(default=False)
    profilePicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage)

    reelLink = models.CharField(max_length=500, default='')
    imdbLink = models.CharField(max_length=500, default='')
    bio = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.username

class Profession(models.Model):
    username = models.CharField(max_length=100)
    professionName = models.CharField(max_length=100)

    def __str__(self):
        return self.professionName

class AbstractPost(models.Model):
    postID = models.CharField(max_length=10)
    poster = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default=None, blank=True, null=True)
    description = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicturePath = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)

class EventPost(AbstractPost):
    location = models.CharField(max_length=1000, default=None, blank=True, null=True)
    date = models.DateField(default=None, blank=True, null=True)

class ProjectPost(AbstractPost):
    status = models.CharField(max_length=50, default=None, blank=True, null=True)

class WorkPost(AbstractPost):
    projectPostID = models.CharField(max_length=10)
    profession = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)

class CollaborationPost(AbstractPost):
    profession = models.CharField(max_length=200)

class CastingPost(AbstractPost):
    # TODO have a separate table for a single casting choice (gender, hair, age, etc)
    paid = models.BooleanField(default=False)


