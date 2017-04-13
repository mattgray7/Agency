from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

import constants
import helpers
import event
import choose
import home
import profile

getBaseContext = helpers.getBaseContext

class GenericAccountView(object):
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
        self._pageContext = None

        self._form = None
        self._formClass = None
        self._formInitialValues = {"source": self.currentPage,
                                   "editSource": self.incomingSource}
        self._formSubmitted = False
        self._formData = None

    @property
    def pageContext(self):
        """To be overridden in parent class"""
        if self._pageContext is None:
            self._pageContext = helpers.getBaseContext(self.request)
        return self._pageContext

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    def setPageContextElement(self, key, value):
        self.pageContext[key] = value

    @property
    def formSubmitted(self):
        self._formSubmitted = self.currentPage == self.incomingSource
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
        """To be overridden in child class"""
        if not self._form:
            if self.formSubmitted:
                self._form = self.formClass(self.request.POST)
            elif self.formClass:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    @property
    def sourcePage(self):
        if self._sourcePage is None:
            if self.formSubmitted:
                self._sourcePage = self.formData.get("editSource")
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

    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                formIsValid = False
                if self.request.POST.get("skip") != "True":
                    if self.formClass:
                        if self.form.is_valid():
                            if self.processForm():
                                formIsValid = True
                    else:
                        if self.processForm():
                            formIsValid = True
                else:
                    formIsValid = True
                if formIsValid:
                    print "processSuccess, redirecting source {0} and current {1}".format(self.sourcePage, self.currentPage)
                    return helpers.redirect(request=self.request,
                                            currentPage=self.currentPage,
                                            sourcePage=self.sourcePage)

        # Need to access before form is set
        self.pageContext
        self._pageContext["form"] = self.form
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)

    def processForm(self):
        """To bo overridden in child class"""
        pass

# Must be done after GenericAccountView defined
import account


def displayHome(request):
    return home.display(request, getBaseContext(request))

def login(request):
    return account.loginUser(request, getBaseContext(request))

def logout(request):
    return account.logoutUser(request, getBaseContext(request))

def createAccount(request):
    return account.createAccount(request, getBaseContext(request))

def editInterests(request):
    view = account.EditInterestsView(request=request, currentPage=constants.EDIT_INTERESTS)
    return view.process()

def editProfessions(request):
    view = account.EditProfessionsView(request=request, currentPage=constants.EDIT_PROFESSIONS)
    return view.process()

def editPicture(request):
    view = account.EditPictureView(request=request, currentPage=constants.EDIT_PROFILE_PICTURE)
    return view.process()
    #return account.editPicture(request, getBaseContext(request))

def editBackground(request):
    view = account.EditBackgroundView(request=request, currentPage=constants.EDIT_BACKGROUND)
    return view.process()

def createAccountFinish(request):
    return account.finish(request, getBaseContext(request))

def createEvent(request):
    return event.create(request, getBaseContext(request))

def choosePostType(request):
    return choose.postType(request, getBaseContext(request))

def browse(request):
    return render(request, "AgencyApp/browse.html", getBaseContext(request))

def displayProfile(request, username):
    return profile.display(request, username, getBaseContext(request))

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})