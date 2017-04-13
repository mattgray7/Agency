from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponseRedirect
from forms import *

from models import UserAccount, Profession
from helpers import getMessageFromKey, capitalizeName

from constants import *
import constants
import helpers
import views

import os

def loginUser(request, context):
    errors = []
    if request.method == 'POST':
        # Form submitted
        form = LoginForm(request.POST)
        if form.is_valid():
            username = _getProfileNameFromEmail(form.cleaned_data.get('email'))
            if username is None:
                errors.append("{0} is not a registered email.".format(form.cleaned_data.get('email')))
            else:
                user = authenticate(username=username, password=form.cleaned_data.get('password'))
                if user is not None:
                    # Login was a success
                    login(request, user)
                    # TODO change the source page if from toolbar                
                    return helpers.redirect(request=request,
                                            currentPage=LOGIN,
                                            sourcePage=HOME,
                                            pageKey=form.cleaned_data.get('loginSuccessDestination'))
                else:
                    errors.append("Email and password do not match.")
        else:
            if request.POST.get("loginSuccessDestination"):
                loginSuccessDestination = request.POST.get("loginSuccessDestination")
                context["form"] = LoginForm(initial={'loginSuccessDestination': loginSuccessDestination})
                if loginSuccessDestination == CREATE_POST:
                    errors.append("You must login to create a post.")
                elif loginSuccessDestination == CREATE_EVENT:
                    errors.append("You must login to create an event.")
    
    if not context.get("form"):
        context["form"] = LoginForm()
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/login.html', context)


def logoutUser(request, context):
    logout(request)
    return HttpResponseRedirect('/')


def createAccount(request, context):
    errors = []
    memory = {}
    memorySource = {}
    incomingSource = _getIncomingSource(request)
    if request.method == 'POST':
        # Form submitted
        form = CreateAccountForm(request.POST)
        if incomingSource == CREATE_BASIC_ACCOUNT:
            if form.is_valid():
                memorySource = form.cleaned_data
                if _emailIsRegistered(form.cleaned_data.get('email')):
                    errors.append("Email already in use.")
                else:
                    if form.cleaned_data.get('password') != form.cleaned_data.get('passwordConfirm'):
                        errors.append("Passwords don't match.")
                    else:
                        firstName = capitalizeName(form.cleaned_data.get('firstName'))
                        lastName = capitalizeName(form.cleaned_data.get('lastName'))
                        username = _getProfileNameFromName(firstName.lower(), lastName.lower())
                        
                        user = User.objects.create_user(username=username,
                                                        email=form.cleaned_data.get('email'), 
                                                        password=form.cleaned_data.get('password'),
                                                        first_name=firstName,
                                                        last_name=lastName)
                        userAccount = UserAccount(email=form.cleaned_data.get('email'),
                                                  username=username,
                                                  firstName=firstName,
                                                  lastName=lastName,
                                                  setupComplete=False)
                        saveSuccess = True
                        try:
                            user.save()
                        except:
                            saveSuccess = False
                            errors.append("Unable to save in User db.")
                        else:
                            try:
                                userAccount.save()
                            except:
                                saveSuccess = False
                                errors.append("Unable to save in UserAccount db.")
                                #TODO delete account from User db
                        if saveSuccess:
                            login(request, user)
                            # TODO change the source (home vs login?)
                            return helpers.redirect(request=request,
                                                    currentPage=CREATE_BASIC_ACCOUNT,
                                                    sourcePage=LOGIN)
            else:
                errors.append("Invalid value entered.")
                memorySource = request.POST

    context["form"] = CreateAccountForm(initial={"email": memorySource.get("email"),
                                                 "firstName": memorySource.get("firstName"),
                                                 "lastName": memorySource.get("lastName"),
                                                 "source": CREATE_BASIC_ACCOUNT,
                                                 "createSource": incomingSource})
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/create.html', context)


def finish(request, context):
    # Get the incoming source and set the destination page
    if request.POST.get("source"):
        # Came from profile page edit
        incomingSource = request.POST.get("source")
    else:
        # Came from editInterests redirect
        incomingSource = getMessageFromKey(request, "source")

    context["showSetupProfile"] = True
    if incomingSource == EDIT_BACKGROUND:
        context["showSetupProfile"] = False
    
    context["possibleSources"] = {"finish": CREATE_BASIC_ACCOUNT_FINISH}

    return render(request, 'AgencyApp/account/finish.html', context)


class EditInterestsView(views.GenericAccountView):
    def __init__(self, *args, **kwargs):
        super(EditInterestsView, self).__init__(*args, **kwargs)

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
            return True
        except:
            self.errors.append("Could not connect to UserAccount database")
        return False


class EditProfessionsView(views.GenericAccountView):
    def __init__(self, *args, **kwargs):
        super(EditProfessionsView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        if self._pageContext is None:
            self._pageContext = helpers.getBaseContext(self.request)
            try:
                self._pageContext["selectedProfessions"] = [x.professionName for x in Profession.objects.filter(username=self.username)]
            except Profession.DoesNotExist:
                self._pageContext["selectedProfessions"] = []

            self._pageContext["professionList"] = PROFESSIONS
            self._pageContext["source"] = EDIT_PROFESSIONS
            self._pageContext["editSource"] = self.incomingSource
        return self._pageContext

    def processForm(self):
        """Overriding asbtract method"""
        professionsSelected = self.formData.getlist("professions")
        Profession.objects.filter(username=self.username).delete()
        for profession in professionsSelected:
            entry = Profession(username=self.username, professionName=profession)
            entry.save()
        return True


def editPicture(request, context):
    errors = []
    incomingSource = _getIncomingSource(request)

    if request.method == "POST":
        form = EditPictureForm(request.POST, request.FILES)
        if request.POST.get("source") == EDIT_PROFILE_PICTURE:
            if form.is_valid():
                userAccount = UserAccount.objects.get(username=request.user.username)
                userAccount.profilePicture = request.FILES['profilePicture']

                # Save the picture in its location
                userAccount.save()

                # TODO 



                # TODO convert image to jpg or other common format
                # Rename the file
                initialPath = userAccount.profilePicture.path
                newName = "profile{0}".format(os.path.splitext(initialPath)[-1])
                newPath = os.path.join(os.path.dirname(initialPath), newName)
                os.rename(initialPath, newPath)

                # Save the new path in the db
                userAccount.profilePicture.name = os.path.join(request.user.username, newName)
                try:
                    userAccount.save()
                    pass
                except:
                    errors.append("Could not connect to UserAccount db.")
                else:
                    return helpers.redirect(request=request,
                                            currentPage=EDIT_PROFILE_PICTURE,
                                            sourcePage=form.cleaned_data.get('editSource'))
            elif request.POST.get("skip") == "True":
                # editDestination is stored in post data of skip form
                return helpers.redirect(request=request,
                                        currentPage=EDIT_PROFILE_PICTURE,
                                        sourcePage=request.POST.get("editSource"))

    context["form"] = EditPictureForm(initial={"source": EDIT_PROFILE_PICTURE,
                                               "editSource": incomingSource})

    # add edit destination to context so that skip button can redirect properly
    context["editSource"] = incomingSource
    context["possibleSources"] = {"picture": EDIT_PROFILE_PICTURE}
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/picture.html', context)


class EditBackgroundView(views.GenericAccountView):
    def __init__(self, *args, **kwargs):
        super(EditBackgroundView, self).__init__(*args, **kwargs)

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



