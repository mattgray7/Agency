from __future__ import unicode_literals

import json
import datetime
from django.db import models
from django.core.files.storage import FileSystemStorage
import helpers
import constants

from django.conf import settings
imageStorage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}/'.format(settings.MEDIA_URL),
)

def image_directory_path(instance, filename):
    if hasattr(instance, "username") and instance.username:
        inputString = instance.username
    elif (isinstance(instance, EventPost) or 
          isinstance(instance, ProjectPost) or
          isinstance(instance, WorkPost) or
          isinstance(instance, CollaborationPost) or
          isinstance(instance, CastingPost) and
          hasattr(instance, "poster")):
        inputString = instance.poster
    else:
        print "WARNING: Using 'mattgray' as username directory to store image {0}".format(filename)
        inputString = "mattgray"  # Temp for create db objects script
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
    def cleanName(self):
        return helpers.capitalizeName("{0} {1}".format(self.firstName, self.lastName))

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

class TempPostPicture(models.Model):
    tempID = models.CharField(max_length=10)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)
    username = models.CharField(max_length=200)


class AbstractPost(models.Model):
    postID = models.CharField(max_length=10)
    projectID = models.CharField(max_length=10, blank=True, null=True)
    poster = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default=None, blank=True, null=True)
    description = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicturePath = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)
    status = models.CharField(max_length=50, default="Open", blank=True, null=True)

class ProjectPost(AbstractPost):
    projectType = models.CharField(max_length=200, blank=True, null=True)
    length = models.CharField(max_length=200, blank=True, null=True)      # only filled if status is Filled (vs Hiring)
    union = models.BooleanField(default=False, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    shortDescription = models.CharField(max_length=200, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(ProjectPost, self).__init__(*args, **kwargs)
        self._openRoles = None
        self._totalRoles = None
        self._openJobs = None
        self._totalJobs = None
        self._directors = None
        self._writers = None
        self._actors = None
        self._producers = None

    @property
    def directors(self):
        if self._directors is None:
            self._directors = [x.workerName for x in WorkPost.objects.filter(projectID=self.projectID, profession="Director")]
        return self._directors

    @property
    def writers(self):
        if self._writers is None:
            self._writers = [x.workerName for x in WorkPost.objects.filter(projectID=self.projectID, profession__in=["Writer", "Screenwriter", "Story writer"])]
        return self._writers

    @property
    def actors(self):
        if self._actors is None:
            self._actors = [x.actorName for x in CastingPost.objects.filter(projectID=self.projectID, status="Cast")]
        return self._actors

    @property
    def producers(self):
        if self._producers is None:
            self._producers = [x.workerName for x in WorkPost.objects.filter(projectID=self.projectID, profession="Producer")]
        return self._producers

    @property
    def openRoles(self):
        if self._openRoles is None:
            #self._openRoles = CastingPost.objects.filter(projectID=self.postID, status="Open")
            self._openRoles = CastingPost.objects.filter(projectID=self.postID, status="Open")
        return self._openRoles

    @property
    def totalRoles(self):
        if self._totalRoles is None:
            #self._totalRoles = CastingPost.objects.filter(projectID=self.postID)
            self._totalRoles = CastingPost.objects.filter(projectID=self.postID)
            print self._totalRoles
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

class ProjectAdmin(models.Model):
    projectID = models.CharField(max_length=10)
    username = models.CharField(max_length=10)

class PostAdmin(models.Model):
    postID = models.CharField(max_length=10)
    username = models.CharField(max_length=10)

class CollaborationPost(AbstractPost):
    collaboratorRole = models.CharField(max_length=200)

class WorkPost(AbstractPost):
    profession = models.CharField(max_length=200)
    workerName = models.CharField(max_length=200, blank=True, null=True)      # only filled if status is Filled (vs Hiring)
    compensationType = models.CharField(default="Unpaid", max_length=200, blank=True, null=True)
    compensationDescription = models.CharField(max_length=200, blank=True, null=True)
    skills = models.CharField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    startDate = models.DateField(default=None, blank=True, null=True)
    endDate = models.DateField(default=None, blank=True, null=True)
    hoursPerWeek = models.TextField(max_length=50, blank=True, null=True, default="TBD")
    workerNeedsEquipment = models.BooleanField(default=True)
    equipmentDescription = models.CharField(max_length=500, blank=True, null=True)

    @property
    def postType(self):
        return constants.WORK_POST

    @property
    def compensation(self):
        if self.compensationType:
            if self.compensationDescription:
                return "{0} - {1}".format(self.compensationType, self.compensationDescription)
            else:
                return self.compensationType
        return "Unspecified"

class CastingPost(AbstractPost):
    compensationType = models.CharField(default="Unpaid", max_length=200, blank=True, null=True)
    compensationDescription = models.CharField(max_length=200, blank=True, null=True)
    descriptionEnabled = models.BooleanField(default=False)
    roleType = models.CharField(max_length=100, default="Acting", blank=True, null=True)
    actorName = models.CharField(max_length=200, blank=True, null=True)
    characterName = models.CharField(max_length=200)
    characterType = models.CharField(max_length=100, default="Actor")
    hairColor = models.CharField(max_length=50, blank=True, null=True)
    eyeColor = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=50, blank=True, null=True)
    ageRange = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    build = models.CharField(max_length=50, blank=True, null=True)
    skills = models.CharField(max_length=300, blank=True, null=True)
    languages = models.CharField(max_length=300, blank=True, null=True)
    startDate = models.DateField(default=None, blank=True, null=True)
    endDate = models.DateField(default=None, blank=True, null=True)
    location = models.CharField(max_length=1000, default=None, blank=True, null=True)
    hoursPerWeek = models.TextField(max_length=50, blank=True, null=True, default="TBD")

    @property
    def postType(self):
        return constants.CASTING_POST

    @property
    def compensation(self):
        if self.compensationType:
            if self.compensationDescription:
                return "{0} - {1}".format(self.compensationType, self.compensationDescription)
            else:
                return self.compensationType
        return "Unspecified"

class EventPost(AbstractPost):
    location = models.CharField(max_length=1000, default=None, blank=True, null=True)
    startDate = models.DateField(default=None, blank=True, null=True)
    endDate = models.DateField(default=None, blank=True, null=True)
    startTime = models.TimeField(default=None, blank=True, null=True)
    endTime = models.TimeField(default=None, blank=True, null=True)
    host = models.CharField(max_length=200, default=None, blank=True, null=True)
    admissionInfo = models.CharField(max_length=200, default=None, blank=True, null=True)

    @property
    def postType(self):
        return constants.EVENT_POST

    @property
    def eventStatus(self):
        eventStatus = "Past"
        currentDate = datetime.datetime.now().date();
        if self.startDate < currentDate and self.endDate < currentDate:
            eventStatus = "Past"
        elif self.startDate == currentDate == self.endDate:
            eventStatus = "Today"
        elif self.startDate < currentDate and self.endDate > currentDate:
            eventStatus = "Happening Now"
        elif self.startDate > currentDate:
            eventStatus = "Upcoming"
        return eventStatus

    @property
    def dateString(self):
        return helpers.getDateString(self.startDate, self.endDate)

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


