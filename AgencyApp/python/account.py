from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponseRedirect
from forms import *

from models import UserAccount, Profession
from helpers import getMessageFromKey

from constants import *
import constants
import helpers
import views

import os


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
        if self.destinationPage == CREATE_POST_CHOICE and postMsg not in self._pageErrors:
            self._pageErrors.append(postMsg)
        elif self.destinationPage == CREATE_EVENT_POST and eventMsg not in self._pageErrors:
            self._pageErrors.append(eventMsg)
        elif self.destinationPage == CREATE_PROJECT_POST and projectMsg not in self._pageErrors:
            self._pageErrors.append(projectMsg)
        return self._pageErrors

    @property
    def formInitialValues(self):
        self._formInitialValues["email"] = self.errorMemory.get("email")
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
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
            self._cancelDestination = HOME
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
                userAccount = UserAccount(email=self.formData.get('email'),
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
        self._pageContext["possibleDestinations"] = {"event": CREATE_EVENT_POST,
                                                     "post": CREATE_POST,
                                                     "browse": BROWSE}
        return self._pageContext

    def checkFormValidity(self):
        return True


class EditInterestsView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(EditInterestsView, self).__init__(*args, **kwargs)

    @property
    def cancelButtonName(self):
        if self.sourcePage != PROFILE:
            self._cancelButtonName = "Skip"
        return self._cancelButtonName

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            if self.destinationPage == EDIT_PROFESSIONS:
                self._cancelDestination = EDIT_PROFESSIONS
            else:
                self._cancelDestination = PROFILE
        return self._cancelDestination

    @property
    def formInitialValues(self):
        self._formInitialValues["work"] = self.userAccount.workInterest
        self._formInitialValues["crew"] = self.userAccount.crewInterest
        self._formInitialValues["collaboration"] = self.userAccount.collaborationInterest
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
        self.userAccount.workInterest = self.formData.get('work', False)
        self.userAccount.crewInterest = self.formData.get('crew', False)
        self.userAccount.collaborationInterest = self.formData.get('collaboration', False)
        try:
            self.userAccount.save()
        except:
            self.errors.append("Could not connect to UserAccount database")
            return False
        return True


class EditProfessionsView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(EditProfessionsView, self).__init__(*args, **kwargs)

    @property
    def cancelButtonName(self):
        if self.sourcePage != PROFILE:
            self._cancelButtonName = "Skip"
        return self._cancelButtonName

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            if self.destinationPage == EDIT_PROFILE_PICTURE:
                self._cancelDestination = EDIT_PROFILE_PICTURE
            else:
                self._cancelDestination = PROFILE
        return self._cancelDestination

    @property
    def pageContext(self):
        try:
            self._pageContext["selectedProfessions"] = [x.professionName for x in Profession.objects.filter(username=self.username)]
        except Profession.DoesNotExist:
            self._pageContext["selectedProfessions"] = []
        self._pageContext["professionList"] = PROFESSIONS
        return self._pageContext

    def processForm(self):
        """Overriding asbtract method"""
        professionsSelected = self.formData.getlist("professions")
        Profession.objects.filter(username=self.username).delete()
        for profession in professionsSelected:
            entry = Profession(username=self.username, professionName=profession)
            try:
                entry.save()
            except:
                return False
        return True


class EditPictureView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        super(EditPictureView, self).__init__(*args, **kwargs)
        self._pictureModel = self.userAccount
        self._pictureModelFieldName = "profilePicture"
        self._filename = None

    @property
    def cancelDestinationURL(self):
        if self._cancelDestinationURL is None:
            self._cancelDestinationURL = constants.URL_MAP.get(self.currentPage)
            if self._cancelDestinationURL:
                self._cancelDestinationURL = self._cancelDestinationURL.format(self.request.user.username)
        return self._cancelDestinationURL

    @property
    def cancelButtonName(self):
        if self.sourcePage != PROFILE:
            self._cancelButtonName = "Skip"
        return self._cancelButtonName

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            if self.destinationPage == EDIT_BACKGROUND:
                self._cancelDestination = EDIT_BACKGROUND
            else:
                self._cancelDestination = PROFILE
        return self._cancelDestination

    @property
    def pageContext(self):
        self._pageContext["userAccount"] = self.userAccount
        return self._pageContext

    @property
    def filename(self):
        if self._filename is None:
            self._filename = MEDIA_FILE_NAME_MAP.get(EDIT_PROFILE_PICTURE, "tempfile")
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


class EditBackgroundView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(EditBackgroundView, self).__init__(*args, **kwargs)

    @property
    def cancelButtonName(self):
        if self.sourcePage != PROFILE:
            self._cancelButtonName = "Skip"
        return self._cancelButtonName

    @property
    def cancelDestination(self):
        """Override to continue the profile setup process"""
        if self._cancelDestination is None:
            if self.destinationPage == HOME:
                self._cancelDestination = HOME
            else:
                self._cancelDestination = PROFILE
        return self._cancelDestination

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
        user = UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
        return None
    else:
        return user.username


def _getProfileNameFromName(firstName, lastName):
    tempName = "{0}{1}".format(firstName, lastName)
    numConflictingNames = len(UserAccount.objects.filter(username__startswith=tempName))
    if numConflictingNames > 0:
        # if mattgray exists, new name will be mattgray1
        tempName += str(numConflictingNames)
    return tempName



