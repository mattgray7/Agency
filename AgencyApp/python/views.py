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

        self._sourcePage = kwargs.get("sourcePage")
        self._currentPage = kwargs.get("currentPage")
        self._destinationPage = None
        self._destPageKey = None

        self._userAccount = None
        self._username = None
        self._pageErrors = []  #TODO

        self.errorMemory = {}

        # Need to setup the base context first so child classes can add to it
        self._pageContext = {}
        self.setupBaseContext()

    def setupBaseContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
        self._pageContext["source"] = self.currentPage
        self._pageContext["next"] = self.currentPage
        self._pageContext["destination"] = self.destinationPage

    @property
    def pageContext(self):
        """To be overridden in child class"""
        self._pageContext["errors"] = self.pageErrors
        return self._pageContext

    @property
    def pageErrors(self):
        "TODO"
        return self._pageErrors

    @property
    def sourcePage(self):
        if self._sourcePage is None:
            if self.request.POST.get("source"):
                self._sourcePage = self.request.POST.get("source")
                print "post request has source, and source page is {0}".format(self._sourcePage)
            else:
                self._sourcePage = helpers.getMessageFromKey(self.request, "source")
                print "message has source, and source page is {0}".format(self._sourcePage)
        return self._sourcePage

    @property
    def currentPage(self):
        if self._currentPage is None:
            if self.request.POST.get("next"):
                self._currentPage = self.request.POST.get("next")
            else:
                self._currentPage = self.sourcePage
        return self._currentPage

    @property
    def destinationPage(self):
        if self._destinationPage is None:
            if self.request.POST.get("destination"):
                self._destinationPage = self.request.POST.get("destination")
            if self._destinationPage in [None, constants.DEFAULT]:
                self._destinationPage = constants.DEFAULT_PAGE_MAP.get(self.currentPage)
        return self._destinationPage

    @property
    def destPageKey(self):
        """Used when multiple destination options for same source and current page combo"""
        return self._destPageKey

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


class GenericFormView(GenericView):
    def __init__(self, *args, **kwargs):
        super(GenericFormView, self).__init__(*args, **kwargs)
        self._form = None
        self._formClass = None
        self._formInitialValues = {}
        self._formSubmitted = False
        self._formData = None
        self._cancelDestination = None

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def formSubmitted(self):
        self._formSubmitted = self.currentPage == self.sourcePage
        return self._formSubmitted

    @property
    def formInitialValues(self):
        # To override in child class
        self._formInitialValues["source"] = self.currentPage
        self._formInitialValues["next"] = self.currentPage
        self._formInitialValues["destination"] = self.destinationPage
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

    @property
    def cancelDestination(self):
        if self._cancelDestination is None:
            self._cancelDestination = self.sourcePage
        return self._cancelDestination

    def checkFormValidity(self):
        formIsValid = False
        if self.request.POST.get(constants.CANCEL) != "True":
            if self.formSubmitted:
                if self.formClass:
                    if self.form.is_valid():
                        self.errorMemory = self.formData
                        formIsValid = self.processForm()
                    else:
                        self.errorMemory = self.request.POST
                else:
                    formIsValid = self.processForm()
        else:
            self._destinationPage = self.cancelDestination
            self._pageContext["destination"] = self.cancelDestination
            formIsValid = True
        return formIsValid

    def process(self):
        if self.request.method == "POST" and self.checkFormValidity():
            return helpers.redirect(request=self.request,
                                    currentPage=self.currentPage,
                                    destinationPage=self.destinationPage)

        # Need to access pageContext before setting variables
        # !!!!!!!!!! Don't delete
        self.pageContext
        # !!!!!!!!!!
        self._pageContext["form"] = self.form
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        print "source :{0}, current: {1}, dest: {2}".format(self.sourcePage, self.currentPage, self.destinationPage)
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)

    def processForm(self):
        """To bo overridden in child class"""
        pass


class PictureFormView(GenericFormView):
    def __init__(self, *args, **kwargs):
        super(PictureFormView, self).__init__(*args, **kwargs)
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

    def checkFormValidity(self):
        formIsValid = False
        if self.request.POST.get(constants.CANCEL) != "True":
            if self.formSubmitted:
                if self.formClass:
                    if self.form.is_valid():
                        self.errorMemory = self.formData
                        if self.processForm():
                            if self.request.FILES.get(self.pictureModelFieldName):
                                if self.updatePicturePathAndModel():
                                    formIsValid = True
                            else:
                                formIsValid = True
                    else:
                        self.errorMemory = self.request.POST
                else:
                    if self.processForm():
                        formIsValid = True
        else:
            #self._destinationPage = self.sourcePage == constants.LOGIN and constants.HOME or self.sourcePage
            self._destinationPage = self.cancelDestination
            formIsValid = True
        return formIsValid

    def updatePicturePathAndModel(self):
        if self.pictureModel:
            # Save the InMemoryUploadedFile instance in the file field of the model
            self._pictureModelPictureField = self.request.FILES.get(self.pictureModelFieldName)
            self.pictureModel.save()

            # Rename event file
            if self.pictureModelPictureField:
                newPath = os.path.join(os.path.dirname(self.pictureModelPictureField.path), self.filename)
                os.rename(self.pictureModelPictureField.path, newPath)
                self._pictureModelPictureField.name = os.path.join(self.request.user.username, self.filename)
                self.pictureModel.save()
                return True
        return False

# Must be done after GenericAccountView defined
import account
import event
import browse


def displayHome(request):
    return home.display(request, getBaseContext(request))

def login(request):
    view = account.LoginView(request=request, currentPage=constants.LOGIN)
    return view.process()

def logout(request):
    view = account.LogoutView(request=request, currentPage=constants.LOGOUT)
    return view.process()

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
    view = account.CreateAccountFinishView(request=request, currentPage=constants.CREATE_BASIC_ACCOUNT_FINISH)
    return view.process()

def createEvent(request):
    view = event.CreateEventView(request=request, currentPage=constants.CREATE_EVENT)
    return view.process()

def editEvent(request, eventID):
    view = event.CreateEventView(request=request, currentPage=constants.CREATE_EVENT, eventID=eventID)
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