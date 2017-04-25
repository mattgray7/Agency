from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

from helpers import getMessageFromKey

from constants import *
import constants
import helpers
import views
import models
import random, string

class CreateEventView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreateEventView, self).__init__(*args, **kwargs)
        self._eventID = kwargs.get('eventID') or self.request.POST.get("eventID")

    @property
    def pageContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
            self._pageContext["eventID"] = self.eventID
            self._pageContext["possibleSources"] = {"login": constants.LOGIN,
                                                    "setupAccountFinish": constants.SETUP_ACCOUNT_FINISH,
                                                    "createBasicAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH}
        return self._pageContext

    @property
    def eventID(self):
        if self._eventID is None:
            tempEventIDValid = False
            while not tempEventIDValid:
                tempEventID = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(constants.EVENT_ID_LENGTH))
                if len(models.Event.objects.filter(eventID = tempEventID)) == 0:
                    self._eventID = tempEventID
                    tempEventIDValid = True
                    break
        return self._eventID

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def formSubmitted(self):
        return self.request.POST.get("title") and self.request.POST.get("description") and self.request.POST.get("location")

    @property
    def formInitialValues(self):
        self._formInitialValues["eventID"] = self.eventID
        self._formInitialValues["poster"] = self.username
        self._formInitialValues["source"] = self.incomingSource
        return self._formInitialValues

    @property
    def form(self):
        if not self._form:
            if self.formSubmitted:
                self._form = self.formClass(self.request.POST)
            else:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                print "form submitted"
                formIsValid = False
                if self.request.POST.get("cancel") != "True":
                    if self.formClass:
                        print "there is a form class, {0}".format(self.formClass)
                        if self.form.is_valid():
                            print "form is valid"
                        if self.processForm():
                            print "process form success"
                            formIsValid = True
                    else:
                        if self.processForm():
                            formIsValid = True
                else:
                    formIsValid = True
                    print "form is Valid because of cancel"
                if formIsValid:
                    print "processSuccess, redirecting source {0} and current {1}, pagekey {2}".format(self.sourcePage,
                                                                                                       self.currentPage,
                                                                                                       self.pageKey)
                    return helpers.redirect(request=self.request,
                                            currentPage=self.currentPage,
                                            sourcePage=self.sourcePage)
        # Need to access pageContext before setting variables
        print "page context is {0}".format(self.pageContext)
        self._pageContext["form"] = self.form
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)

    def processForm(self):
        print "processingform"
        title = self.formData.get("title", "")
        poster = self.formData.get("poster", "")
        location = self.formData.get("location", "")
        description = self.formData.get("description", "")
        if len(title) < 1:  #TODO switch min length
            self._pageErrors.append("Title must be at least 30 characters long.")
        else:
            if poster != self.username:
                self._pageErrors.append("You must be logged in to create an event.")
            else:
                if len(description) < 1:  #TODO switch min length
                    self._pageErrors.append("Event description must be at least 75 characters long.")
                else:
                    if location < 1:  #TODO switch min length
                        self._pageErrors.append("Location must be at least 20 characters long.")
                    else:
                        newEvent = models.Event(eventID = self.eventID,
                                                poster=poster,
                                                title=title,
                                                location=location,
                                                description=description
                                                )
                        try:
                            newEvent.save()
                            print "saved new event with eventID {0}".format(self.eventID)
                        except Excetion as e:
                            print e
                            self._pageErrors.append("Could not connect to Event database.")
                        else:
                            return True
        print "returning false"
        return False


class ViewEventView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(ViewEventView, self).__init__(*args, **kwargs)

        self._eventID = kwargs.get("eventID")
        self._currentEvent = None

    @property
    def eventID(self):
        return self._eventID

    @property
    def pageContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
            self._pageContext["event"] = self.currentEvent
        return self._pageContext

    @property
    def currentEvent(self):
        if self._currentEvent is None:
            self._currentEvent = models.Event.objects.get(eventID=self.eventID)
        return self._currentEvent

    def process(self):
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)

