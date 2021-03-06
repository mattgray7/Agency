from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponseRedirect
from forms import *

import models
import constants
import helpers
import genericViews as views

import post_casting as castingPost
import profile
import os
import copy
from itertools import chain

import actorDescription


class LoginView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)

    @property
    def userAccount(self):
        return None

    @property
    def pageErrors(self):
        postMsg = "You must login to create a post."
        eventMsg = "You must login to create an event."
        projectMsg = "You must login to create a project."
        if self.destinationPage == constants.CREATE_POST_CHOICE and postMsg not in self._pageErrors:
            self._pageErrors.append(postMsg)
        elif self.destinationPage == constants.CREATE_EVENT_POST and eventMsg not in self._pageErrors:
            self._pageErrors.append(eventMsg)
        elif self.destinationPage == constants.CREATE_PROJECT_POST and projectMsg not in self._pageErrors:
            self._pageErrors.append(projectMsg)
        return self._pageErrors

    @property
    def formInitialValues(self):
        self._formInitialValues["email"] = self.errorMemory.get("email")
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
        if not self.request.POST.get("ajax", False):
            self._username = _getProfileNameFromEmail(self.formData.get('email'))
            if self._username is None:
                self._pageErrors.append("{0} is not a registered email.".format(self.formData.get('email')))
            else:
                user = authenticate(username=self.username, password=self.formData.get('password'))
                if user is not None:
                    # Login was a success
                    login(self.request, user)
                    return True
                else:
                    self._pageErrors.append("Email and password do not match.")
        return False
 

class LogoutView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(LogoutView, self).__init__(*args, **kwargs)

    @property
    def userAccount(self):
        return None

    def process(self):
        username = self.username  # Need to access before using in filter
        logout(self.request)
        try:
            userAccount = models.UserAccount.objects.get(username=username)
        except models.UserAccount.DoesNotExist:
            pass
        else:
            userAccount.lastLogout = datetime.datetime.now()
            userAccount.save()
        return helpers.redirect(request=self.request,
                                currentPage=self.currentPage,
                                destinationPage=self.destinationPage)


class CreateAccountView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreateAccountView, self).__init__(*args, **kwargs)

    @property
    def userAccount(self):
        return None

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            self._cancelDestination = constants.HOME
        return self._cancelDestination

    @property
    def pageContext(self):
        self._pageContext["email"] = self.errorMemory.get("email")
        self._pageContext["firstName"] = self.errorMemory.get("firstName")
        self._pageContext["lastName"] = self.errorMemory.get("lastName")
        self._pageContext["phoneNumber"] = self.errorMemory.get("phoneNumber")
        return self._pageContext

    @property
    def formInitialValues(self):
        self._formInitialValues["email"] = self.errorMemory.get("email")
        self._formInitialValues["firstName"] = self.errorMemory.get("firstName")
        self._formInitialValues["lastName"] = self.errorMemory.get("lastName")
        self._formInitialValues["phoneNumber"] = self.errorMemory.get("phoneNumber")
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
        print "RPOCESSING CREATE FORM"
        if _emailIsRegistered(self.formData.get('email')):
            self._pageErrors.append("Email already in use.")
        else:
            if self.formData.get('password') != self.formData.get('passwordConfirm'):
                self._pageErrors.append("Passwords don't match.")
            else:
                firstName = helpers.capitalizeName(self.formData.get('firstName'))
                lastName = helpers.capitalizeName(self.formData.get('lastName'))
                self._username = _getProfileNameFromName(firstName.lower(), lastName.lower())
                user = User.objects.create_user(username=self.username,
                                                email=self.formData.get('email'),
                                                password=self.formData.get('password'),
                                                first_name=firstName,
                                                last_name=lastName)
                userAccount = models.UserAccount(email=self.formData.get('email'),
                                                 username=self.username,
                                                 firstName=firstName,
                                                 lastName=lastName,
                                                 phoneNumber=self.formData.get("phoneNumber"),
                                                 setupComplete=False)
                try:
                    user.save()
                    userAccount.save()
                except Exception as e:
                    print e
                    self._pageErrors.append("Unable to create User.")
                else:
                    login(self.request, user)
                    return True
        return False


class CreateAccountFinishView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreateAccountFinishView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext["possibleDestinations"] = {"event": constants.CREATE_EVENT_POST,
                                                     "post": constants.CREATE_POST,
                                                     "browse": constants.BROWSE}
        return self._pageContext

    def checkFormValidity(self):
        return True


class InboxView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(InboxView, self).__init__(*args, **kwargs)
        self._messages = None

    """
    If user1 sends a message to user 2 --> user1: sent, user2: inbox
    if user2 responds to messages --> user1: inbox (original message in sent), user2:inbox (response message in sent)

    """

    def cancelPage(self):
        pass

    @property
    def messages(self):
        if self._messages is None:
            messagesDict = {"inbox": [], "sent": []}
            for conversation in self.userAccount.conversations:
                latestOwnMessage = conversation.getLatestOwnMessage(self.userAccount.username)
                if latestOwnMessage:
                    # If user has written a message, add his latest written message to sent list
                    messagesDict["sent"].append(self._formatMessageDict(latestOwnMessage))
                    if conversation.bothUsersResponded:
                        # If other person responded (ie conversation started), put in inbox
                        if conversation.latestMessage.sender == self.userAccount.username and conversation.latestMessage.applicationMessage:
                            messagesDict["inbox"].append(self._formatMessageDict(latestOwnMessage))
                        else:
                            messagesDict["inbox"].append(self._formatMessageDict(conversation.latestMessage))
                else:
                    # User hasn't written any messages, so just appear in inbox
                    messagesDict["inbox"].append(self._formatMessageDict(conversation.latestMessage))
            # Sort the message lists by sent time
            self._messages = {"inbox": sorted(messagesDict["inbox"], key=lambda k: k['sentTime'], reverse=True),
                              "sent": sorted(messagesDict["sent"], key=lambda k: k['sentTime'], reverse=True)}
        return self._messages

    @property
    def pageContext(self):
        self._pageContext = super(InboxView, self).pageContext
        self._pageContext["messages"] = json.dumps(self.messages)
        self._pageContext["possibleDestinations"] = {"viewPost": constants.VIEW_POST,
                                                     "profile": constants.PROFILE}
        return self._pageContext

    def _formatMessageDict(self, message):
        messageDict = {}
        if message:
            try:
                sender = models.UserAccount.objects.get(username=message.sender)
                recipient = models.UserAccount.objects.get(username=message.recipient)
            except models.UserAccount.DoesNotExist:
                pass
            else:
                messageDict = {"messageID": message.messageID,
                               "conversationID": message.conversationID,
                               "sender": {"username": sender.username,
                                          "cleanName": sender.cleanName,
                                          "profileProfession": sender.mainProfession,
                                          "profilePictureURL": sender.profilePicture and sender.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH},
                               "recipient": {"username": recipient.username,
                                             "cleanName": recipient.cleanName,
                                             "profileProfessions": recipient.mainProfession,
                                             "profilePictureURL": recipient.profilePicture and recipient.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH},
                               "content": message.content,
                               "sentTime": message.sentTime.strftime('%s'),
                               "unread": not message.recipientSeen,
                               "applicationMessage": message.applicationMessage,
                               }
        return messageDict


class GenericEditAccountView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(GenericEditAccountView, self).__init__(*args, **kwargs)
        self._nextButtonString = None

    @property
    def nextButtonString(self):
        return self._nextButtonString

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.currentPage
        return self._cancelSource

    def cancelPage(self):
        pass

    @property
    def cancelButtonName(self):
        if self.sourcePage != constants.PROFILE:
            self._cancelButtonName = "Skip"
        else:
            self._cancelButtonName = "Back"
        return self._cancelButtonName

    @property
    def cancelDestinationURL(self):
        if self._cancelDestinationURL is None:
            self._cancelDestinationURL = constants.URL_MAP.get(self.currentPage)
            if self._cancelDestinationURL and self.cancelDestination == constants.PROFILE:
                self._cancelDestinationURL = self._cancelDestinationURL.format(self.request.user.username)
        return self._cancelDestinationURL

    @property
    def pageContext(self):
        self._pageContext = super(views.GenericFormView, self).pageContext
        self._pageContext["nextButtonString"] = self.nextButtonString

        newDestinations = {"interests": constants.EDIT_INTERESTS,
                           "picture": constants.EDIT_PROFILE_PICTURE,
                           "profile": constants.PROFILE, 
                           "background": constants.EDIT_BACKGROUND,
                           "filmography": constants.EDIT_FILMOGRAPHY}
        if "possibleDestinations" in self._pageContext:
            self._pageContext["possibleDestinations"].update(newDestinations)
        else:
            self._pageContext["possibleDestinations"] = newDestinations
        self._pageContext["userAccount"] = self.userAccount
        return self._pageContext

class EditInterestsView(GenericEditAccountView):
    def __init__(self, *args, **kwargs):
        super(EditInterestsView, self).__init__(*args, **kwargs)
        self._existingProfessions = None
        self._existingHiringInterests = None
        self._existingAvailability = None

    @property
    def pageContext(self):
        self._pageContext = super(EditInterestsView, self).pageContext
        self._pageContext["professions"] = constants.PROFESSIONS
        self._pageContext["existingProfessions"] = self.existingProfessions
        self._pageContext["existingHiringInterests"] = self.existingHiringInterests
        self._pageContext["existingAvailability"] = self.existingAvailability
        return self._pageContext

    @property
    def existingAvailability(self):
        if self._existingAvailability is None:
            if self.userAccount:
                if self.userAccount.availability:
                    self._existingAvailability = self.userAccount.availability
        return self._existingAvailability

    @property
    def existingProfessions(self):
        if self._existingProfessions is None:
            self._existingProfessions = models.Interest.objects.filter(username=self.username, mainInterest="work")
        return self._existingProfessions

    @property
    def existingHiringInterests(self):
        if self._existingHiringInterests is None:
            self._existingHiringInterests = models.Interest.objects.filter(username=self.username, mainInterest="hire")
        return self._existingHiringInterests

    @property
    def nextButtonString(self):
        if self._nextButtonString is None:
            if self.sourcePage == constants.PROFILE:
                self._nextButtonString = "Update interests"
            else:
                self._nextButtonString = "Add interests"
        return self._nextButtonString

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            if self.destinationPage == constants.EDIT_PROFILE_PICTURE:
                self._cancelDestination = constants.EDIT_PROFILE_PICTURE
            else:
                self._cancelDestination = constants.PROFILE
        return self._cancelDestination

    def getProfessionInterest(self, profession):
        for interest in constants.PROFESSIONS:
            if profession in constants.PROFESSIONS[interest]:
                return interest

    def processForm(self):
        """Overriding asbtract method"""
        interestType = self.request.POST.get("interestType", "work")

        if interestType == "other":
            # Delete all work and hire interests
            models.Interest.objects.filter(username=self.username, mainInterest="work").delete()
            models.Interest.objects.filter(username=self.username, mainInterest="hire").delete()
        else:
            # Just delete the existing interests for what you are about to edit
            models.Interest.objects.filter(username=self.username, mainInterest=interestType).delete()

        # Delete all other interests (if still set to other, will be re-added)
        models.Interest.objects.filter(username=self.username, mainInterest="other").delete()

        if interestType == "work":
            for formInput in self.request.POST:
                if formInput.startswith("profession."):
                    profession = formInput.split(".")[1]
                    subInterest = self.getProfessionInterest(profession)
                    matchingProfessions = models.Interest.objects.filter(username=self.username, mainInterest=interestType,
                                                                           subInterest=subInterest, professionName=profession)
                    if not matchingProfessions:
                        newProfession = models.Interest(username=self.username, mainInterest=interestType,
                                                        subInterest=subInterest, professionName=profession)
                        newProfession.save()
                elif formInput.startswith("availability."):
                    # Save availability information
                    if formInput.startswith("availability.openAvailability"):
                        self._userAccount.availabilityType = "openAvailability";
                        self._userAccount.save()

                        # Delete existing weekdays
                        models.AvailableWeekday.objects.filter(username=self.username).delete()

                        # Delete existing availability dates
                        models.AvailabilityDate.objects.filter(username=self.username).delete()
                    elif formInput.startswith("availability.weekday."):
                        self._userAccount.availabilityType = "daysOfWeek";
                        self._userAccount.save()
                        weekday = formInput.split(".")[2]
                        repeatValue = self.request.POST.get("availabilityWeekdayRepeat")
                        if repeatValue:
                            if repeatValue in constants.AVAILABILITY_REPEAT_WEEK_VALUES:
                                repeatWeeks = constants.AVAILABILITY_REPEAT_WEEK_VALUES.get(repeatValue)
                                createNew = False
                                try:
                                    weekdayObject = models.AvailableWeekday.objects.get(username=self.username, weekday=weekday)
                                    if weekdayObject.repeatWeeks == repeatWeeks:
                                        weekdayObject.delete()
                                        createNew = True
                                except models.AvailableWeekday.DoesNotExist:
                                    createNew = True

                                if createNew:
                                    weekdayObject = models.AvailableWeekday(username=self.username, weekday=weekday, repeatWeeks=repeatWeeks)
                                    weekdayObject.save()
                    elif formInput.startswith("availability.datesList."):
                        splitted = formInput.split(".")
                        if len(splitted) > 2:
                            datesType = splitted[2]
                            self._userAccount.availabilityType = "specifyDates_{0}".format(datesType);
                            self._userAccount.save()

                            # Delete existing availability dates
                            models.AvailabilityDate.objects.filter(username=self.username).delete()
                            dateList = json.loads(formInput.replace("availability.datesList.{0}.".format(datesType), ""))

                            for date in dateList:
                                dateObject = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                                try:
                                    newDay = models.AvailabilityDate.objects.get(username=self.username, date=dateObject)
                                except models.AvailabilityDate.DoesNotExist:
                                    newDay = models.AvailabilityDate(username=self.username, date=dateObject)
                                    newDay.save()
        elif interestType == "hire":
            for formInput in self.request.POST:
                if formInput.startswith("hireType."):
                    hireType = formInput.split(".")[1]
                    newHireInterests = models.Interest.objects.filter(username=self.username, mainInterest=interestType,
                                                                      subInterest=hireType)
                    if not newHireInterests:
                        newHireInterest = models.Interest(username=self.username, mainInterest=interestType,
                                                          subInterest=hireType)
                        newHireInterest.save()
        elif interestType == "other":
            newOtherInterests = models.Interest.objects.filter(username=self.username, mainInterest=interestType)
            if not newOtherInterests:
                newOtherInterest = models.Interest(username=self.username, mainInterest=interestType)
                newOtherInterest.save()
        return True


class EditPictureView(GenericEditAccountView, views.PictureFormView):
    def __init__(self, *args, **kwargs):
        super(EditPictureView, self).__init__(*args, **kwargs)
        self._pictureModel = self.userAccount
        self._pictureModelFieldName = "profilePicture"
        self._filename = None

    @property
    def nextButtonString(self):
        if self._nextButtonString is None:
            if self.sourcePage == constants.PROFILE:
                self._nextButtonString = "Update profile picture"
            else:
                self._nextButtonString = "Add profile picture"
        return self._nextButtonString

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            if self.destinationPage == constants.EDIT_BACKGROUND:
                self._cancelDestination = constants.EDIT_BACKGROUND
            else:
                self._cancelDestination = constants.PROFILE
        return self._cancelDestination

    @property
    def pageContext(self):
        self._pageContext = super(EditPictureView, self).pageContext
        self._pageContext["profileMediaPictures"] = self.userAccount.profileMediaPictures
        return self._pageContext

    @property
    def filename(self):
        if self._filename is None:
            self._filename = constants.MEDIA_FILE_NAME_MAP.get(constants.EDIT_PROFILE_PICTURE, "tempfile")
        return self._filename

    def processForm(self):
        """Overriding asbtract method"""
        if self.request.FILES.get("profilePicture"):
            self.userAccount.profilePicture = self.request.FILES.get("profilePicture")

        try:
            self.userAccount.save()
        except Exception as e:
            print e
            self._pageErrors.append("Could not connect to User database")
        else:
            return True
        return False


class EditBackgroundView(GenericEditAccountView):
    def __init__(self, *args, **kwargs):
        super(EditBackgroundView, self).__init__(*args, **kwargs)
        self._selectFields = None
        self._physicalAttributeData = None

    @property
    def pageContext(self):
        self._pageContext = super(EditBackgroundView, self).pageContext
        self._pageContext["selectFields"] = json.dumps(self.selectFields)
        self._pageContext["profileProfessions"] = json.dumps(self.userAccount.profileProfessions)
        self._pageContext["physicalAttributeProfessions"] = constants.PROFESSIONS.get("acting")
        self._pageContext["physicalAttributeData"] = self.physicalAttributeData
        return self._pageContext

    @property
    def physicalAttributeData(self):
        if self._physicalAttributeData is None:
            self._physicalAttributeData = []
            omitFields = ["ageRange", "characterType"]
            for attribute in constants.ACTOR_ATTRIBUTE_DICT:
                if attribute["name"] not in omitFields:
                    newAttribute = copy.deepcopy(attribute)
                    newAttribute["value"] = self.formInitialValues.get(attribute["name"])
                    self._physicalAttributeData.append(newAttribute)
            self._physicalAttributeData = [{"name": "dateOfBirth",
                                            "label": "Date of Birth",
                                            "value": self.formInitialValues.get("dateOfBirth")}] + self._physicalAttributeData
        return self._physicalAttributeData

    @property
    def nextButtonString(self):
        if self._nextButtonString is None:
            if self.sourcePage == constants.PROFILE:
                self._nextButtonString = "Update background"
            else:
                self._nextButtonString = "Add background information"
        return self._nextButtonString

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.sourcePage
        return self._cancelSource

    """@property
    def destinationPage(self):
        if self._destinationPage is None:
            if self.userAccount.actorInterest:
                if constants.PROFILE in [self.sourcePage, self.request.POST.get("destination")]:
                    self._destinationPage = constants.PROFILE
                else:
                    self._destinationPage = constants.EDIT_ACTOR_DESCRIPTION
            else:
                self._destinationPage = constants.PROFILE
        return self._destinationPage"""

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        return constants.PROFILE

    @property
    def formInitialValues(self):
        self._formInitialValues["imdbLink"] = self.userAccount.imdbLink
        self._formInitialValues["bio"] = self.userAccount.bio
        #self._formInitialValues["mainProfession"] = self.userAccount.mainProfession
        self._formInitialValues["location"] = self.userAccount.location
        self._formInitialValues["dateOfBirth"] = self.userAccount.dateOfBirth
        self._formInitialValues["education"] = self.userAccount.education
        self._formInitialValues["gender"] = self.userAccount.gender
        self._formInitialValues["resume"] = self.userAccount.resume
        self._formInitialValues["hairColor"] = self.userAccount.hairColor
        self._formInitialValues["eyeColor"] = self.userAccount.eyeColor
        self._formInitialValues["ethnicity"] = self.userAccount.ethnicity
        self._formInitialValues["build"] = self.userAccount.build
        self._formInitialValues["height"] = self.userAccount.height
        self._formInitialValues["phoneNumber"] = self.userAccount.phoneNumber
        return self._formInitialValues

    @property
    def selectFields(self):
        if self._selectFields is None:
            self._selectFields = {"gender": constants.GENDER_OPTIONS}
        return self._selectFields

    def processForm(self):
        """Overriding asbtract method"""
        self.userAccount.imdbLink = self.request.POST.get('imdbLink')
        self.userAccount.bio = self.formData.get('bio')
        self.userAccount.location = self.formData.get('location')
        self.userAccount.education = self.formData.get('education')

        # Have to use request.POST cause physical attributes not included in FormClass
        defaultSelectValue = "-"
        self.userAccount.gender = self.request.POST.get('gender') != defaultSelectValue and self.request.POST.get("gender") or None
        self.userAccount.hairColor = self.request.POST.get("hairColor") != defaultSelectValue and self.request.POST.get("hairColor") or None
        self.userAccount.eyeColor = self.request.POST.get("eyeColor") != defaultSelectValue and self.request.POST.get("eyeColor") or None
        self.userAccount.ethnicity = self.request.POST.get("ethnicity") != defaultSelectValue and self.request.POST.get("ethnicity") or None
        self.userAccount.build = self.request.POST.get("build") != defaultSelectValue and self.request.POST.get("build") or None
        self.userAccount.height = self.request.POST.get("height")
        self.userAccount.phoneNumber = self.request.POST.get("phoneNumber")

        if self.request.POST.get("dateOfBirth"):
            self.userAccount.dateOfBirth = self.request.POST.get('dateOfBirth')

        # Want to delete all professions if profession list is an empty list, so continue as long as field name is present in request
        if self.request.POST.get("professionList", "None") != "None":
            # Delete existing professions
            models.ProfileProfession.objects.filter(username=self.userAccount.username).delete()
            if self.request.POST.get("professionList"):
                professionList = json.loads(self.request.POST.get("professionList"))
            else:
                professionList = []

            for profession in professionList:
                # Add new profession
                profileProfession = models.ProfileProfession(username=self.userAccount.username,
                                                             profession=profession)
                profileProfession.save()

        # Remove existing resume if it exists (can remove existing and add new in same form submission)
        if self.request.POST.get("removeResumeFile", "false") in ["true", "True", True]:
            if self.userAccount.resume and self.userAccount.resume.path:
                os.remove(self.userAccount.resume.path)
            self.userAccount.resume = None

        if self.request.FILES and self.request.FILES.get('resume'):
            self.userAccount.resume = self.request.FILES.get('resume')
        try:
            self.userAccount.save()
            return True
        except Exception as e:
            print e
            self._pageErrors.append("Could not connect to UserAccount database")
        return False


class EditFilmographyView(GenericEditAccountView):
    def __init__(self, *args, **kwargs):
        super(EditFilmographyView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext = super(EditFilmographyView, self).pageContext
        self._pageContext["projectTypes"] = constants.PROJECT_TYPE_LIST
        self._pageContext["projectStatusList"] = json.dumps(constants.PROJECT_STATUS_LIST)
        self._pageContext["profileProjects"] = json.dumps(self.userAccount.projects)
        self._pageContext["possibleDestinations"]["createProject"] = constants.CREATE_PROJECT_POST
        self._pageContext["possibleDestinations"]["viewPost"] = constants.VIEW_POST
        return self._pageContext

    @property
    def nextButtonString(self):
        if self._nextButtonString is None:
            if self.sourcePage == constants.PROFILE:
                self._nextButtonString = "Update Filmography"
            else:
                self._nextButtonString = "Add Filmography"
        return self._nextButtonString

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.sourcePage
        return self._cancelSource

    """@property
    def destinationPage(self):
        if self._destinationPage is None:
            if self.userAccount.actorInterest:
                if constants.PROFILE in [self.sourcePage, self.request.POST.get("destination")]:
                    self._destinationPage = constants.PROFILE
                else:
                    self._destinationPage = constants.EDIT_ACTOR_DESCRIPTION
            else:
                self._destinationPage = constants.PROFILE
        return self._destinationPage"""

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        return constants.PROFILE

    def processForm(self):
        """Overriding asbtract method"""
        return True


class EditActorDescriptionView(GenericEditAccountView):
    def __init__(self, *args, **kwargs):
        super(EditActorDescriptionView, self).__init__(*args, **kwargs)
        self._attributes = None
        self._attributeListObject = None

    @property
    def attributeListObject(self):
        if self._attributeListObject is None:
            self._attributeListObject = actorDescription.ProfileAttributes(request=self.request, username=self.username, pageType=constants.PROFILE)
        return self._attributeListObject

    @property
    def destinationPage(self):
        if self._destinationPage is None:
            self._destinationPage = constants.PROFILE
        return self._destinationPage

    @property
    def nextButtonString(self):
        if self._nextButtonString is None:
            if self.sourcePage == constants.PROFILE:
                self._nextButtonString = "Update physical description"
            else:
                self._nextButtonString = "Add physical description"
        return self._nextButtonString

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        return constants.PROFILE

    @property
    def pageContext(self):
        self._pageContext["attributes"] = self.attributeListObject.attributes
        self._pageContext["descriptionEnabled"] = self.userAccount.actorDescriptionEnabled
        return self._pageContext

    def processForm(self):
        """Overriding asbtract method"""
        self.attributeListObject.save()
        return True


def _getIncomingSource(request):
    if request.POST.get("source"):
        incomingSource = request.POST.get("source")
    else:
        incomingSource = getMessageFromKey(request, "source")
    return incomingSource


def _emailIsRegistered(email):
    existingUsers = User.objects.filter(email=email)
    return len(existingUsers) > 0


def _getProfileNameFromEmail(email):
    try:
        user = models.UserAccount.objects.get(email=email)
    except models.UserAccount.DoesNotExist:
        return None
    else:
        return user.username


def _getProfileNameFromName(firstName, lastName):
    tempName = "{0}{1}".format(firstName, lastName)
    numConflictingNames = len(models.UserAccount.objects.filter(username__startswith=tempName))
    if numConflictingNames > 0:
        # if mattgray exists, new name will be mattgray1
        tempName += str(numConflictingNames)
    return tempName



