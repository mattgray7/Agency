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
        self.pageContext = helpers.getBaseContext(self.request)

        self._form = None
        self._formClass = None
        self._formInitialValues = {"source": self.currentPage,
                                   "editSource": self.incomingSource}
        self._formSubmitted = False
        self._formData = None

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    def setFormClass(self, formClass):
        self._formClass = formClass

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
            if self.request.method == "POST":
                if self.formSubmitted:
                    self._form = self.formClass(self.request.POST)
                else:
                    self._form = self.formClass(initial=self.formInitialValues)
                    print "initial values are {0}".format(self.formInitialValues)
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
            print "request is post"
            if self.formSubmitted:
                print "form is submitted"
                if self.form.is_valid():
                    print "form is valid"
                    if self.processForm():
                        print "processSuccess, redirecting source {0} and current {1}".format(self.sourcePage, self.currentPage)
                        return helpers.redirect(request=self.request,
                                                currentPage=self.currentPage,
                                                sourcePage=self.sourcePage)
        self.pageContext["form"] = self.form
        return render(self.request, 'AgencyApp/account/interests.html', self.pageContext)

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

def editPicture(request):
    return account.editPicture(request, getBaseContext(request))

def editProfessions(request):
    return account.editProfessions(request, getBaseContext(request))

def editBackground(request):
    return account.editBackground(request, getBaseContext(request))

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