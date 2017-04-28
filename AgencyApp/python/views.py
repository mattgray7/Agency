from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import constants
import helpers
import choose
import home
import profile
import models

import os

getBaseContext = helpers.getBaseContext

class GenericView(object):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        if not self.request:
            # TODO raise proper exception
            raise("No request passed to view")

        self._incomingSource = None
        self._sourcePage = kwargs.get("sourcePage")
        self._currentPage = kwargs.get("currentPage")

        self._userAccount = None
        self._username = None
        self._pageErrors = []  #TODO

        self.errorMemory = {}
        self._pageContext = {}
        self._pageKey = None

    @property
    def pageContext(self):
        """To be overridden in child class"""
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
        return self._pageContext

    @property
    def pageKey(self):
        """The page key for page destination"""
        return self._pageKey

    @property
    def pageErrors(self):
        "TODO"
        return self._pageErrors

    @property
    def sourcePage(self):
        if self._sourcePage is None:
            if self.formSubmitted:
                self._sourcePage = self.request.POST.get("editSource") or self.request.POST.get("createSource") or self.request.POST.get("loginSource")
            else:
                self._sourcePage = self.incomingSource
        return self._sourcePage

    @property
    def currentPage(self):
        if self._currentPage is None:
            self._currentPage = self.incomingSource
        return self._currentPage

    @property
    def incomingSource(self):
        if self._incomingSource is None:
            if self.request.POST.get("source"):
                self._incomingSource = self.request.POST.get("source")
                print "incoming source is {0}".format(self._incomingSource)
                print self.request.POST
            else:
                self._incomingSource = helpers.getMessageFromKey(self.request, "source")
        return self._incomingSource

    @property
    def userAccount(self):
        if self._userAccount is None:
            self._userAccount = UserAccount.objects.get(username=self.username)
        return self._userAccount

    @property
    def username(self):
        if self._username is None:
            self._username = self.request.user.username
        return self._username


class PictureFormView(object):
    def __init__(self, *args, **kwargs):
        print "in picture form view init"
        self.request = kwargs.get("request")
        self._pictureModel = None
        self._pictureModelPictureField = None
        self._pictureModelFieldName = None
        self._filename = None

    @property
    def filename(self):
        if self._filename is None:
            self._filename = MEDIA_FILE_NAME_MAP.get(self.request.POST.get("source"), "tempfile")
        return self._filename

    @property
    def pictureModel(self):
        # like event
        return self._pictureModel

    @property
    def pictureModelPictureField(self):
        # like event.eventPicture
        # Need to return updated field each time is accessed (since the field is set independently)
        self._pictureModelPictureField = self.pictureModel.__dict__[self.pictureModelFieldName]
        return self._pictureModelPictureField

    @property
    def pictureModelFieldName(self):
        # Like eventPicture
        return self._pictureModelFieldName

    def updatePicturePathAndModel(self):
        if self.pictureModel:
            # Save the InMemoryUploadedFile instance in the file field of the model
            self._pictureModelPictureField = self.request.FILES.get(self.pictureModelFieldName)
            self.pictureModel.save()

            # Rename event file
            if self.pictureModelPictureField:
                newPath = os.path.join(os.path.dirname(self.pictureModelPictureField.path), self.filename)
                print "newPath is {0}".format(newPath)
                os.rename(self.pictureModelPictureField.path, newPath)
                print "renamed path {0} to newpath {1}".format(self.pictureModelPictureField.path, newPath)

                self._pictureModelPictureField.name = os.path.join(self.request.user.username, self.filename)
                print "Set picture model field.name to {0}".format(self._pictureModelPictureField.name)
                self.pictureModel.save()
                return True
        return False


class GenericFormView(GenericView):
    def __init__(self, *args, **kwargs):
        super(GenericFormView, self).__init__(*args, **kwargs)
        self._form = None
        self._formClass = None
        self._formInitialValues = {"source": self.currentPage,
                                   "editSource": self.incomingSource,
                                   "createSource": self.incomingSource}
        self._formSubmitted = False
        self._formData = None

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def formSubmitted(self):
        self._formSubmitted = self.currentPage == self.incomingSource
        print "current, source: {0} {1}".format(self.currentPage, self.incomingSource)
        return self._formSubmitted

    @property
    def formInitialValues(self):
        # To override in child class
        return self._formInitialValues

    @property
    def formData(self):
        if self._formData is None:
            if self.formClass is None:
                self._formData = self.request.POST
            else:
                self._formData = self.form.is_valid() and self.form.cleaned_data
        return self._formData

    @property
    def form(self):
        if not self._form:
            if self.formSubmitted:
                self._form = self.formClass(self.request.POST)
            elif self.formClass:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                formIsValid = False
                if self.request.POST.get("skip") != "True":
                    if self.formClass:
                        if self.form.is_valid():
                            self.errorMemory = self.formData
                            if self.processForm():
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

    def processForm(self):
        """To bo overridden in child class"""
        pass

# Must be done after GenericAccountView defined
import account
import event
import browse


def displayHome(request):
    return home.display(request, getBaseContext(request))

def login(request):
    return account.loginUser(request, getBaseContext(request))

def logout(request):
    return account.logoutUser(request, getBaseContext(request))

def createAccount(request):
    view = account.CreateAccountView(request=request, currentPage=constants.CREATE_BASIC_ACCOUNT)
    return view.process()

def editInterests(request):
    view = account.EditInterestsView(request=request, currentPage=constants.EDIT_INTERESTS)
    return view.process()

def editProfessions(request):
    view = account.EditProfessionsView(request=request, currentPage=constants.EDIT_PROFESSIONS)
    return view.process()

def editPicture(request):
    view = account.EditPictureView(request=request, currentPage=constants.EDIT_PROFILE_PICTURE)
    return view.process()

def editBackground(request):
    view = account.EditBackgroundView(request=request, currentPage=constants.EDIT_BACKGROUND)
    return view.process()

def createAccountFinish(request):
    return account.finish(request, getBaseContext(request))

def createEvent(request):
    view = event.CreateEventView(request=request, sourcePage=constants.HOME, currentPage=constants.CREATE_EVENT)
    return view.process()

def editEvent(request, eventID):
    view = event.CreateEventView(request=request, sourcePage=constants.VIEW_EVENT, currentPage=constants.CREATE_EVENT, eventID=eventID)
    return view.process()

def viewEvent(request, eventID):
    view = event.ViewEventView(request=request, currentPage=constants.VIEW_EVENT, eventID=eventID)
    return view.process()

def choosePostType(request):
    return choose.postType(request, getBaseContext(request))

def browseEvents(request):
    view = browse.BrowseEventsView(request=request, sourcePage=constants.HOME, currentPage=constants.BROWSE_EVENTS)
    return view.process()

def browsePosts(request):
    return render(request, "AgencyApp/browse.html", getBaseContext(request))

def displayProfile(request, username):
    return profile.display(request, username, getBaseContext(request))

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})