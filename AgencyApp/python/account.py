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
import os
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
 

class LogoutView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(LogoutView, self).__init__(*args, **kwargs)

    @property
    def userAccount(self):
        return None

    def process(self):
        logout(self.request)
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
        return self._pageContext

    @property
    def formInitialValues(self):
        self._formInitialValues["email"] = self.errorMemory.get("email")
        self._formInitialValues["firstName"] = self.errorMemory.get("firstName")
        self._formInitialValues["lastName"] = self.errorMemory.get("lastName")
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
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
                                                     "browse": constants.BROWSE_CHOICE}
        return self._pageContext

    def checkFormValidity(self):
        return True


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
        self._pageContext["nextButtonString"] = self.nextButtonString
        return self._pageContext

class EditInterestsView(GenericEditAccountView):
    def __init__(self, *args, **kwargs):
        super(EditInterestsView, self).__init__(*args, **kwargs)
        self._existingInterests = None

    @property
    def pageContext(self):
        self._pageContext = super(EditInterestsView, self).pageContext
        self._pageContext["possibleDestinations"] = {"interests": constants.EDIT_INTERESTS}
        self._pageContext["professions"] = constants.PROFESSIONS
        return self._pageContext

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
            if self.destinationPage == constants.EDIT_PROFESSIONS:
                self._cancelDestination = constants.EDIT_PROFESSIONS
            else:
                self._cancelDestination = constants.PROFILE
        return self._cancelDestination

    @property
    def existingInterests(self):
        if self._existingInterests is None:
            userInterests = models.Interest.objects.filter(username=self.username)
            self._existingInterests = {"work": [], "hire": []}
            for interest in userInterests:
                self._existingInterests[interest.name].append(interest.subInterestName)
        return self._existingInterests

    def processForm(self):
        """Overriding asbtract method"""
        self.userAccount.workInterest = self.formData.get('work', False)
        self.userAccount.crewInterest = self.formData.get('crew', False)
        self.userAccount.collaborationInterest = self.formData.get('collaboration', False)
        self.userAccount.actingInterest = self.formData.get("acting", False)
        self.userAccount.castingInterest = self.formData.get("casting", False)
        try:
            self.userAccount.save()
        except:
            self.errors.append("Could not connect to UserAccount database")
            return False
        return True


class EditProfessionsView(GenericEditAccountView):
    def __init__(self, *args, **kwargs):
        super(EditProfessionsView, self).__init__(*args, **kwargs)

    @property
    def nextButtonString(self):
        if self._nextButtonString is None:
            if self.sourcePage == constants.PROFILE:
                self._nextButtonString = "Update professions"
            else:
                self._nextButtonString = "Add interested professions"
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

    @property
    def pageContext(self):
        try:
            self._pageContext["selectedProfessions"] = [x.professionName for x in models.Profession.objects.filter(username=self.username)]
        except models.Profession.DoesNotExist:
            self._pageContext["selectedProfessions"] = []
        self._pageContext["professionList"] = constants.PROFESSIONS
        return self._pageContext

    def processForm(self):
        """Overriding asbtract method"""
        professionsSelected = self.formData.getlist("professions")
        models.Profession.objects.filter(username=self.username).delete()
        for profession in professionsSelected:
            entry = models.Profession(username=self.username, professionName=profession)
            try:
                entry.save()
            except Exception as e:
                print "Could not create profession entry: {0}".format(e)
                return False
        return True


class EditPictureView(GenericEditAccountView):
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
        self._pageContext["userAccount"] = self.userAccount
        return self._pageContext

    @property
    def filename(self):
        if self._filename is None:
            self._filename = MEDIA_FILE_NAME_MAP.get(constants.EDIT_PROFILE_PICTURE, "tempfile")
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

    @property
    def destinationPage(self):
        if self._destinationPage is None:
            if self.userAccount.actingInterest:
                if constants.PROFILE in [self.sourcePage, self.request.POST.get("destination")]:
                    self._destinationPage = constants.PROFILE
                else:
                    self._destinationPage = constants.EDIT_ACTOR_DESCRIPTION
            else:
                self._destinationPage = constants.PROFILE
        return self._destinationPage

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        return self.destinationPage

    @property
    def formInitialValues(self):
        self._formInitialValues["reel"] = self.userAccount.reelLink
        self._formInitialValues["imdb"] = self.userAccount.imdbLink
        self._formInitialValues["bio"] = self.userAccount.bio
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
        self.userAccount.reelLink = self.formData.get('reel')
        self.userAccount.imdbLink = self.formData.get('imdb')
        self.userAccount.bio = self.formData.get('bio')
        try:
            self.userAccount.save()
            return True
        except:
            self.errors.append("Could not connect to UserAccount database")
        return False


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



