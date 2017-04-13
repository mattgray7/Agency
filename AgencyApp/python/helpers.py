from django.contrib import messages
from django.shortcuts import render

from django.http import HttpResponseRedirect
import constants
from models import UserAccount


class GenericAccountView(object):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        print "request is {0}".format(self.request)
        if not self.request:
            # TODO raise proper exception
            raise("No request passed to view")

        self._incomingSource = None
        self._sourcePage = kwargs.get("sourcePage")
        self._currentPage = kwargs.get("currentPage")

        self._userAccount = None
        self._username = None
        self._pageErrors = []  #TODO
        self.pageContext = getBaseContext(self.request)

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
                self._incomingSource = getMessageFromKey(self.request, "source")
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
                        return redirect(request=self.request,
                                        currentPage=self.currentPage,
                                        sourcePage=self.sourcePage)
        self.pageContext["form"] = self.form
        return render(self.request, 'AgencyApp/account/interests.html', self.pageContext)

    def processForm(self):
        """To bo overridden in child class"""
        pass

class EditInterestsView(GenericAccountView):
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
        print "overridden method now"
        workSelected = self.formData.get('work', False)
        crewSelected = self.formData.get('crew', False)
        collabSelected = self.formData.get('collaboration', False)
        self.userAccount.workInterest = workSelected
        self.userAccount.crewInterest = crewSelected
        self.userAccount.collaborationInterest = collabSelected
        try:
            self.userAccount.save()
            return True
        except:
            self.errors.append("Could not connect to UserAccount database")
        return False


def redirect(request, currentPage, sourcePage, pageKey=None):
    """Returns an HttpResonseRedirect of the desired URL can be resolved (see getDestinationURL for 
    more info on how this is done). If no URL can be resolved, an error is raised

    :param request: The request object
    :param str currentPage: Current page name as defined in constants.py
    :param str sourcePage: Name of page that led to the current page as defined in constants.py
    :param str pageKey: Optional argument if multiple destinations exist from the same current/source
                        page combintaion, defaults to DEFAULT
    :return HttpResonseRedirect: Redirect to destination if found
    """
    if None in [currentPage, sourcePage]:
        print "Current or source page not specified"
        #TODO raise proper exception
        raise

    destinationURL = getDestinationURL(currentPage, sourcePage, pageKey, request.user.username)
    if not destinationURL:
        print "No url could be resolved"
        raise
    else:
        messages.add_message(request, messages.INFO,
                             "source:{0}".format(currentPage))
        return HttpResponseRedirect(destinationURL)


def getDestinationURL(currentPage, sourcePage, pageKey=None, username=None):
    """Returns a destination URL taken from the PAGE_MAP dict declared in constants.py.
    The URL is determined from the current page requesting the URL, and the source page
    that led to the current page. If there could be multiple, different destinations from
    the same currentPage and sourcePage, the pageKey is used to determine the correct one. 
    Otherwise, the default page for the current/source combo is used

    :param str currentPage: Current page name as defined in constants.py
    :param str sourcePage: Name of page that led to the current page as defined in constants.py
    :param str pageKey: Optional argument if multiple destinations exist from the same current/source
                        page combintaion, defaults to DEFAULT
    :param str username: Optional argument if the destination could be profile requiring a username
    :return str: Relative URL defined in the URL_MAP in constants.py
    """
    if not pageKey:
        pageKey = constants.DEFAULT

    currentPageMap = constants.PAGE_MAP.get(currentPage)
    if currentPageMap:
        destPageMap = currentPageMap.get(sourcePage)
        if destPageMap:
            destPageName = destPageMap.get(pageKey)
            if destPageName:
                destURL = constants.URL_MAP.get(destPageName)
                # Special case for profile
                #TODO get the username without haveing to pass the request
                if destPageName == constants.PROFILE:
                    if username:
                        destURL = destURL.format(username)
                    else:
                        print "USERNAME SHOULD HAVE BEEN PASSED"
                        destURL = "/"
                if destURL:
                    return destURL
                else:
                    print "helpers.py: getDestinationURL: no destURL found"
            else:
                print "helpers.py: getDestinationURL: no destPageName found"
        else:
            print "helpers.py: getDestinationURL: no destPageMap found"
    else:
        print "helpers.py: getDestinationURL: no currentPageMap found"


def getBaseContext(request):
    """Returns context required by the base template.

    :return dict: Context required by base.html
    """
    if request.POST:
        source = request.POST.get("source")
    else:
        source = getMessageFromKey(request, "source")
    return {"toolbarSources": {"login": constants.TOOLBAR_LOGIN,
                               "home": constants.TOOLBAR_HOME,
                               "logout": constants.TOOLBAR_LOGOUT,
                               "profile": constants.TOOLBAR_PROFILE},
            "source": source
            }


def getMessageFromKey(request, key):
    """Returns the value of a key included in a message object.

    :param WSGIRequest request: The request to get the message from
    :param str key: The key to return the value for
    :return: The value of the key, None if key doesn't exist
    """
    messagesList = messages.get_messages(request)
    for message in messagesList:
    	# TODO convert unicode messages.messages to dict
    	splitted = message.message.split(":")
        if splitted[0] == key:
            return splitted[1]
    return None


def capitalizeName(name):
    """Capitalizes first letter of names (eg matt gray->Matt Gray, smith-pelly->Smith-Pelly, 
       deBrincat->DeBrincat)

    :param str name: The name to capitalize
    :return str: The capitalized name
    """
    finalName = ''
    first = True
    for char in name:
        if first:
            finalName += char.upper()
            first = False
        elif char in ['-', ' ']:
            finalName += char
            first=True
        else:
            finalName += char
    return finalName
