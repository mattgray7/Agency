from __future__ import unicode_literals

import json
import datetime
from django.db import models
from django.core.files.storage import FileSystemStorage
import helpers
import constants
import post
import datetime

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
    phoneNumber = models.CharField(max_length=30, blank=True, null=True)
    setupComplete = models.BooleanField(default=False)

    profilePicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    #reelLink = models.CharField(max_length=500, default='')
    imdbLink = models.CharField(max_length=500, default=None, blank=True, null=True)
    bio = models.CharField(max_length=1000, default='')
    location = models.CharField(max_length=200, default='')
    education = models.CharField(max_length=200, default='')
    resume = models.FileField(default=None, blank=True, null=True, upload_to=image_directory_path, storage=imageStorage)

    gender = models.CharField(max_length=200, blank=True, null=True)
    dateOfBirth = models.DateField(default=None, blank=True, null=True)
    hairColor = models.CharField(max_length=100, default=None, blank=True, null=True)
    eyeColor = models.CharField(max_length=100, default=None, blank=True, null=True)
    ethnicity = models.CharField(max_length=100, default=None, blank=True, null=True)
    build = models.CharField(max_length=100, default=None, blank=True, null=True)
    height = models.CharField(max_length=100, default=None, blank=True, null=True)
    def __init__(self, *args, **kwargs):
        super(UserAccount, self).__init__(*args, **kwargs)
        self._actorInterest = None
        self._workInterest = None
        self._hireInterest = None
        self._otherInterest = None
        self._projects = None
        self._profileProfessions = None
        self._profileMediaPictures = None
        self._profileEndorsements = None
        self._mainProfession = None
        self._actorDescriptionEnabled = None

    def __str__(self):
        return self.username

    @property
    def profileEndorsements(self):
        if self._profileEndorsements is None:
            self._profileEndorsements = []
            endorsements = ProfileEndorsement.objects.filter(username=self.username)
            for endorsement in endorsements:
                newEndorsement = {"postID": endorsement.postID,
                                  "username": endorsement.username,
                                  "description": endorsement.description,
                                  "createdAt": endorsement.createdAt.isoformat()[0: 10]
                                  }
                try:
                    poster = UserAccount.objects.get(username=endorsement.poster)
                except models.UserAccount.DoesNotExist:
                    continue
                else:
                    newEndorsement["poster"] = {"username": poster.username,
                                                "profession": poster.mainProfession,
                                                "cleanName": poster.cleanName,
                                                "profilePictureURL": poster.profilePicture and poster.profilePicture.url or None,
                                                }
                    self._profileEndorsements.append(newEndorsement)
        return self._profileEndorsements

    @property
    def actorDescriptionEnabled(self):
        if self._actorDescriptionEnabled is None:
            self._actorDescriptionEnabled = False

            # Check if actor profession chosen
            actorProfession = False
            for profile in self.profileProfessions:
                if profile in constants.PROFESSIONS.get("acting"):
                    actorProfession = True
                    break

            # If actor profession chosen, check if there is a non-None value in the actor description fields
            if actorProfession:
                # Check to see if any physical values are not None
                for field in [self.gender, self.dateOfBirth, self.hairColor, self.eyeColor, self.ethnicity, self.build, self.height]:
                    if field:
                        self._actorDescriptionEnabled = True
                        break
        return self._actorDescriptionEnabled

    @property
    def profileMediaPictures(self):
        if self._profileMediaPictures is None:
            self._profileMediaPictures = []
            for picture in ProfileMediaPicture.objects.filter(username=self.username):
                self._profileMediaPictures.append({"url": picture.postPicture and picture.postPicture.url or "",
                                                   "id": picture.pictureID,
                                                   "description": picture.description,
                                                   "featured": picture.featured,
                                                   "poster": self.username,
                                                   "createdAt": picture.createdAt.isoformat()[0: 10]})
        return self._profileMediaPictures

    @property
    def hasFeaturedMediaPictures(self):
        # Have to check each time, cause list could have changed between calls
        if self.profileMediaPictures:
            return any(x["featured"] for x in self.profileMediaPictures)
        return False

    @property
    def profileProfessions(self):
        if self._profileProfessions is None:
            self._profileProfessions = [x.profession for x in ProfileProfession.objects.filter(username=self.username)]
        return self._profileProfessions

    @property
    def mainProfession(self):
        # More legacy than anything
        if self._mainProfession is None:
            if self.profileProfessions:
                professionString = ' | '.join(self.profileProfessions)
            else:
                professionString = ''
            self._mainProfession = professionString
        return self._mainProfession

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

    @property
    def projects(self):
        """ Returns a dict of all projects the user is associated with. Searches project participants, project sub-post
        participants, casting post actorNames, and work post workerNames.
        """
        if self._projects is None:
            self._projects = {}

            # Search post participants to find participating projects
            participants = PostParticipant.objects.filter(username=self.username)
            for part in participants:
                newProjectID = part.postID
                labels = []

                # If participant post is not a project (ie is casting or work), check if there is a project associated
                if not post.isProjectPost(part.postID):
                    userPost = post.getPost(part.postID)
                    if hasattr(userPost, "projectID") and userPost.projectID:
                        newProjectID = userPost.projectID
                        if post.isCastingPost(part.postID):
                            labels.append({"label": userPost.characterType, "extra": userPost.characterName})
                        elif post.isWorkPost(part.postID):
                            labels.append({"label": userPost.profession})
                else:
                    labels.append({"label": part.status})

                if newProjectID in self._projects:
                    self._projects[newProjectID]["labels"] += labels
                else:
                    self._projects[newProjectID] = {"labels": labels, "display": part.publicParticipation}

            roles = CastingPost.objects.filter(actorName=self.username)
            for role in roles:
                if role.projectID:
                    newLabelAddition = {"label": role.characterType, "extra": role.characterName}
                    if role.projectID in self._projects:
                        """if any(newLabelAddition["label"] == x["label"] for x in self._projects[role.projectID]["labels"]):
                        #    self._projects[role.projectID]["labels"].append(newLabelAddition)
                            print "adding {0}".format(newLabelAddition)
                            #self._projects[role.projectID]["labels"].append(newLabelAddition)"""
                    else:
                        self._projects[role.projectID] = {"labels": [newLabelAddition], "display": True}

            jobs = WorkPost.objects.filter(workerName=self.username)
            for job in jobs:
                if job.projectID:
                    if job.projectID in self._projects:
                        self._projects[job.projectID]["labels"].append({"label": job.profession})
                    else:
                        self._projects[job.projectID] = {"labels": [{"label": job.profession}], "display": True}

            unregProjects = UnregisteredProject.objects.filter(poster=self.username)
            for project in unregProjects:
                self._projects[project.postID] = {"labels": [{"label": project.profession}], "display": True}

            removeProjectIDList = []
            for projectID in self._projects:
                pictureURL = None
                registeredProject = False
                try:
                    currentProject = ProjectPost.objects.get(postID=projectID)
                    pictureURL = currentProject.postPicture and currentProject.postPicture.url or constants.NO_PICTURE_PATH
                    registeredProject = True
                except ProjectPost.DoesNotExist:
                    try:
                        currentProject = UnregisteredProject.objects.get(postID=projectID)
                        pictureURL = constants.NO_PICTURE_PATH
                    except UnregisteredProject.DoesNotExist:
                        removeProjectIDList.append(projectID)
                        continue
                self._projects[projectID]["name"] = currentProject.title
                self._projects[projectID]["year"] = currentProject.year
                self._projects[projectID]["postPictureURL"] = pictureURL
                self._projects[projectID]["status"] = currentProject.status
                self._projects[projectID]["projectType"] = currentProject.projectType
                self._projects[projectID]["projectID"] = projectID
                self._projects[projectID]["registered"] = registeredProject
            if removeProjectIDList:
                for projectID in removeProjectIDList:
                    del self._projects[projectID]
        return self._projects

class UnregisteredProject(models.Model):
    postID = models.CharField(max_length=10)
    poster = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default=None, blank=True, null=True)
    projectType = models.CharField(max_length=50, default=None, blank=True, null=True)
    status = models.CharField(max_length=50, default=None, blank=True, null=True)
    profession = models.CharField(max_length=300, default=None, blank=True, null=True)
    year = models.CharField(max_length=300, blank=True, null=True)

# Chosen as primary (has filmography, has worked in the past)
class ProfileProfession(models.Model):
    username = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)

class ProfileMediaPicture(models.Model):
    pictureID = models.CharField(max_length=10)
    username = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

class ProfileEndorsement(models.Model):
    postID = models.CharField(max_length=10)
    username = models.CharField(max_length=100)
    poster = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

# Interest is being considered for roles in this position
class Interest(models.Model):
    username = models.CharField(max_length=100)
    mainInterest = models.CharField(max_length=100) #work/hire/other
    subInterest = models.CharField(max_length=100) #acting/onset/offset/preprod/creative/postprod or #hiring/hiring_permanent/casting/collaborating
    professionName = models.CharField(max_length=100)   # only for work interest
    actingDescriptionEnabled = models.BooleanField(default=False)      #only for acting interests

    def __str__(self):
        return self.professionName


class Message(models.Model):
    messageID = models.CharField(max_length=10)
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    recipientSeen = models.BooleanField(default=False)
    subject = models.CharField(max_length=200, default=None, blank=True, null=True)
    content = models.CharField(max_length=10000)
    sentTime = models.DateTimeField(auto_now_add=True)


class AbstractPost(models.Model):
    postID = models.CharField(max_length=10)
    projectID = models.CharField(max_length=10, blank=True, null=True)
    poster = models.CharField(max_length=200)
    title = models.CharField(max_length=500, default=None, blank=True, null=True)
    description = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicturePath = models.CharField(max_length=5000, default=None, blank=True, null=True)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)
    status = models.CharField(max_length=50, default="Open", blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class TempPostPicture(models.Model):
    tempID = models.CharField(max_length=10)
    postPicture = models.ImageField(default=None, upload_to=image_directory_path, storage=imageStorage, blank=True, null=True)
    username = models.CharField(max_length=200)

class PostParticipant(models.Model):
    postID = models.CharField(max_length=10)
    username = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default=None, blank=True, null=True)
    publicParticipation = models.BooleanField(default=False, blank=True, null=True)

class ProjectPost(AbstractPost):
    projectType = models.CharField(max_length=200, blank=True, null=True)
    compensation = models.CharField(default="Unpaid", max_length=200, blank=True, null=True)
    union = models.CharField(max_length=500, default=None, blank=True, null=True)
    startDate = models.DateField(default=None, blank=True, null=True)
    endDate = models.DateField(default=None, blank=True, null=True)
    productionNotes = models.CharField(max_length=5000, default=None, blank=True, null=True)
    companyName = models.CharField(max_length=500, default=None, blank=True, null=True)

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
        self._year = None

    @property
    def year(self):
        if self._year is None:
            if self.endDate:
                self._year = self.endDate.year
            elif self.startDate:
                self._year = self.startDate.year
            else:
                self._year = datetime.datetime.now().year
        return self._year

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
            self._openJobs = WorkPost.objects.filter(projectID=self.postID, status="Open")
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
    startDate = models.DateField(default=None, blank=True, null=True)
    endDate = models.DateField(default=None, blank=True, null=True)
    startTime = models.TimeField(default=None, blank=True, null=True)
    endTime = models.TimeField(default=None, blank=True, null=True)
    host = models.CharField(max_length=200, default=None, blank=True, null=True)
    admissionInfo = models.CharField(max_length=200, default=None, blank=True, null=True)
    eventType = models.CharField(max_length=200, default="Other", blank=True, null=True)

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


