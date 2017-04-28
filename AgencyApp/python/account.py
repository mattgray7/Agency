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
    context["source"] = LOGIN
    return render(request, 'AgencyApp/account/login.html', context)


def logoutUser(request, context):
    logout(request)
    return HttpResponseRedirect('/')


class CreateAccountView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreateAccountView, self).__init__(*args, **kwargs)

    @property
    def userAccount(self):
        return None

    @property
    def pageContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
            self._pageContext["email"] = self.errorMemory.get("email")
            self._pageContext["firstName"] = self.errorMemory.get("firstName")
            self._pageContext["lastName"] = self.errorMemory.get("lastName")
            self._pageContext["createSource"] = self.incomingSource
            self._pageContext["source"] = CREATE_BASIC_ACCOUNT
        return self._pageContext

    @property
    def formInitialValues(self):
        self._formInitialValues["email"] = self.errorMemory.get("email")
        self._formInitialValues["firstName"] = self.errorMemory.get("firstName")
        self._formInitialValues["lastName"] = self.errorMemory.get("lastName")
        self._formInitialValues["createSource"] = self.incomingSource
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


class EditInterestsView(views.GenericFormView):
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
        except:
            self.errors.append("Could not connect to UserAccount database")
            return False
        return True


class EditProfessionsView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(EditProfessionsView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        if not self._pageContext:
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
            try:
                entry.save()
            except:
                print "PROCESS ERROR"
                return False
        return True


class EditPictureView(views.GenericFormView, views.PictureFormView):
    def __init__(self, *args, **kwargs):
        super(EditPictureView, self).__init__(*args, **kwargs)

        self._pictureModel = self.userAccount
        #self._pictureModelPictureField = self.userAccount.profilePicture
        self._pictureModelFieldName = "profilePicture"
        self._filename = None
        self._incomingSource = self.request.POST.get("source")
        print self.request.POST


    @property
    def pageContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
            self._pageContext["userAccount"] = self.userAccount
            self._pageContext["editSource"] = self.incomingSource
            self._pageContext["source"] = EDIT_PROFILE_PICTURE
        return self._pageContext

    @property
    def filename(self):
        if self._filename is None:
            self._filename = MEDIA_FILE_NAME_MAP.get(EDIT_PROFILE_PICTURE, "tempfile")
            self._filename = self._filename.format(os.path.splitext(self.pictureModelPictureField.path)[-1])
            print "FILENAME IS {0}".format(self._filename)
        return self._filename

    @property
    def sourcePage(self):
        self._sourcePage = self.incomingSource
        return self._sourcePage

    @property
    def form(self):
        """To be overridden in child class"""
        if not self._form:
            if self.formSubmitted:
                # Override form to create form with request.FILES
                self._form = self.formClass(self.request.POST, self.request.FILES)
            elif self.formClass:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    @property
    def formSubmitted(self):
        #return self.request.POST.get("title") and self.request.POST.get("description") and self.request.POST.get("location")
        self._formSubmitted = self.sourcePage == self.currentPage
        print "source :{0}, current {1}".format(self.sourcePage, self.currentPage)
        return self._formSubmitted

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def formInitialValues(self):
        self._formInitialValues["source"] = EDIT_PROFILE_PICTURE
        self._formInitialValues["editSource"] = self.incomingSource
        self._formInitialValues["editDestination"] = self.request.POST.get("editDestination")
        #if self.userAccount.profilePicture:
        #    self._formInitialValues["profilePicture"] = self.userAccount.profilePicture.path # TODO add default image
                
        return self._formInitialValues

    def processForm(self):
        """Overriding asbtract method"""
        self.userAccount.profilePicture = self.request.FILES['profilePicture']
        self.userAccount.save()

        # TODO convert image to jpg or other common format
        # Rename the file
        initialPath = self.userAccount.profilePicture.path
        newName = "profile{0}".format(os.path.splitext(initialPath)[-1])
        newPath = os.path.join(os.path.dirname(initialPath), newName)
        os.rename(initialPath, newPath)

        # Save the new path in the db
        self.userAccount.profilePicture.name = os.path.join(self.username, newName)
        try:
            self.userAccount.save()
        except:
            errors.append("Could not connect to UserAccount db.")
            return False
        return True

    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                formIsValid = False
                if self.request.POST.get("skip") != "True":
                    if self.formClass:
                        if self.form.is_valid():
                            self.errorMemory = self.formData
                            if self.processForm() and self.updatePicturePathAndModel():
                                formIsValid = True
                        else:
                            self.errorMemory = self.request.POST
                    else:
                        if self.processForm():
                            formIsValid = True
                else:
                    formIsValid = True
                    print "form is Valid"
                if formIsValid:
                    print "processSuccess, redirecting source {0} and current {1}".format(self.sourcePage, self.currentPage)
                    return helpers.redirect(request=self.request,
                                            currentPage=self.currentPage,
                                            sourcePage=self.sourcePage,
                                            pageKey=self._pageKey)
        # Need to access before form is set
        self.pageContext
        self._pageContext["form"] = self.form
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)



class EditBackgroundView(views.GenericFormView):
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



