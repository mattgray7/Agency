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

    profilePicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage)
    
    actorDescriptionEnabled = models.BooleanField(default=False)        # enabled physical description

    reelLink = models.CharField(max_length=500, default='')
    imdbLink = models.CharField(max_length=500, default='')
    bio = models.CharField(max_length=1000, default='')
    mainProfession = models.CharField(max_length=200, default='')

    def __init__(self, *args, **kwargs):
        super(UserAccount, self).__init__(*args, **kwargs)
        self._actorInterest = None
        self._workInterest = None
        self._hireInterest = None
        self._otherInterest = None

    def __str__(self):
        return self.username

    @property
    def actorInterest(self):
        if self._actorInterest is None:
            try:
                actorInterest = Interest.objects.get(username=self.username, mainInterest="work", subInterest="acting", professionName="Actor")
            except Interest.DoesNotExist:
                self._actorInterest = False
            else:
                self._actorInterest = True
        return self._actorInterest

    @property
    def workInterest(self):
        if self._workInterest is None:
            workInterests = Interest.objects.filter(username=self.username, mainInterest="work")
            if workInterests:
                self._workInterest = True
            else:
                self._workInterest = False
        return self._workInterest

    @property
    def hireInterest(self):
        if self._hireInterest is None:
            hireInterests = Interest.objects.filter(username=self.username, mainInterest="hire")
            if hireInterests:
                self._hireInterest = True
            else:
                self._hireInterest = False
        return self._hireInterest

    @property
    def otherInterest(self):
        if self._otherInterest is None:
            try:
                otherInterest = Interest.objects.get(username=self.username, mainInterest="other")
            except Interest.DoesNotExist:
                self._otherInterest = False
            else:
                self._othernterest = True
        return self._otherInterest


class Interest(models.Model):
    username = models.CharField(max_length=100)
    mainInterest = models.CharField(max_length=100) #work/hire/other
    subInterest = models.CharField(max_length=100) #acting/onset/offset/preprod/creative/postprod or #hiring/hiring_permanent/casting/collaborating
    professionName = models.CharField(max_length=100)   # only for work interest
    actingDescriptionEnabled = models.BooleanField(default=False)      #only for acting interests

    def __str__(self):
        return self.professionName

class AbstractPost(models.Model):
    postID = models.CharField(max_length=10)
    projectID = models.CharField(max_length=10, blank=True, null=True)
    poster = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default=None, blank=True, null=True)
    description = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicturePath = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)
    status = models.CharField(max_length=50, default="Open", blank=True, null=True)

class EventPost(AbstractPost):
    location = models.CharField(max_length=1000, default=None, blank=True, null=True)
    date = models.DateField(default=None, blank=True, null=True)

class ProjectPost(AbstractPost):
    def __init__(self, *args, **kwargs):
        super(ProjectPost, self).__init__(*args, **kwargs)
        self._openRoles = None
        self._totalRoles = None
        self._openJobs = None
        self._totalJobs = None

    @property
    def openRoles(self):
        if self._openRoles is None:
            self._openRoles = CastingPost.objects.filter(projectID=self.postID, status="Open")
        return self._openRoles

    @property
    def totalRoles(self):
        if self._totalRoles is None:
            self._totalRoles = CastingPost.objects.filter(projectID=self.postID)
        return self._totalRoles

    @property
    def openJobs(self):
        if self._openJobs is None:
            self._openJobs = WorkPost.objects.filter(projectID=self.postID, status="Hiring")
        return self._openJobs

    @property
    def totalJobs(self):
        if self._totalJobs is None:
            self._totalJobs = WorkPost.objects.filter(projectID=self.postID)
        return self._totalJobs

class WorkPost(AbstractPost):
    profession = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)

class CollaborationPost(AbstractPost):
    collaboratorRole = models.CharField(max_length=200)

class CastingPost(AbstractPost):
    paid = models.BooleanField(default=False)
    descriptionEnabled = models.BooleanField(default=False)

class Actor(models.Model):
    username = models.CharField(max_length=200)

class ActorDescriptionStringAttribute(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    postID = models.CharField(max_length=200, blank=True, null=True)
    attributeName = models.CharField(max_length=200)
    attributeValue = models.CharField(max_length=200)

class ActorDescriptionBooleanAttribute(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    postID = models.CharField(max_length=200, blank=True, null=True)
    attributeName = models.CharField(max_length=200)
    attributeValue = models.BooleanField(default=False)

class PostFollow(models.Model):
    postID = models.CharField(max_length=10)
    username = models.CharField(max_length=200)


