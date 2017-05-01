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

import os

class CreateEventView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        super(CreateEventView, self).__init__(*args, **kwargs)
        self._eventID = kwargs.get('eventID') or self.request.POST.get("eventID")
        self._formClass = constants.FORM_MAP.get(self.currentPage)
        self._currentEvent = None

        self._pictureModel = self.currentEvent
        self._pictureModelFieldName = "eventPicture"
        self._filename = None

    @property
    def pageContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
            self._pageContext["eventID"] = self.eventID
            self._pageContext["possibleSources"] = {"login": constants.LOGIN,
                                                        "viewEvent": constants.VIEW_EVENT,
                                                        "setupAccountFinish": constants.SETUP_ACCOUNT_FINISH,
                                                        "createBasicAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH}
            self._pageContext["currentEvent"] = self.currentEvent
            self._pageContext["source"] = self.sourcePage  # keep as source in page context, so cancel has correct source
            self._pageContext["next"] = self.currentPage
            self._pageContext["destination"] = self.destinationPage
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
    def formInitialValues(self):
        self._formInitialValues["eventID"] = self.eventID
        self._formInitialValues["poster"] = self.username
        self._formInitialValues["source"] = self.currentPage # set the form source to current page, since it will be the source when the form is submitted and the next page loads
        self._formInitialValues["next"] = self.currentPage
        self._formInitialValues["destination"] = self.destinationPage
        if self.currentEvent:
            self._formInitialValues["title"] = self.currentEvent.title
            self._formInitialValues["description"] = self.currentEvent.description
            self._formInitialValues["location"] = self.currentEvent.location
            self._formInitialValues["date"] = self.currentEvent.date
        return self._formInitialValues

    @property
    def filename(self):
        if self._filename is None:
            self._filename = MEDIA_FILE_NAME_MAP.get(self.request.POST.get("source"), "tempfile")
            self._filename = self._filename.format(self.eventID)
        return self._filename

    @property
    def currentEvent(self):
        if self._currentEvent is None:
            try:
                self._currentEvent = models.Event.objects.get(eventID=self.eventID)
            except models.Event.DoesNotExist:
                self._currentEvent = models.Event(eventID=self.eventID,
                                                  poster=self.request.user.username)
                self._currentEvent.save()
        return self._currentEvent

    @property
    def cancelDestination(self):
        if self._cancelDestination is None:
            if self.sourcePage == SETUP_ACCOUNT_FINISH:
                self._cancelDestination = HOME
            elif self.sourcePage in [LOGIN, CREATE_BASIC_ACCOUNT_FINISH]:
                self._cancelDestination = HOME
            else:
                self._cancelDestination = self.sourcePage
        return self._cancelDestination

    def processForm(self):
        title = self.formData.get("title", "")
        poster = self.formData.get("poster", "")
        location = self.formData.get("location", "")
        description = self.formData.get("description", "")
        date = self.formData.get("date", "")
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
                        if self.currentEvent:
                            # Edit existing event
                            self._currentEvent.title = title
                            self._currentEvent.description = description
                            self._currentEvent.location = location
                            self._currentEvent.date = date
                            if self.request.FILES.get("eventPicture"):
                                self._currentEvent.eventPicture = self.request.FILES.get("eventPicture")
                                print "EVENT PICTURE: {0}".format(self.request.FILES.get("eventPicture"))
                            try:
                                self.currentEvent.save()
                                print "saved new event with eventID {0}".format(self.eventID)
                            except Exception as e:
                                print e
                                self._pageErrors.append("Could not connect to Event database.")
                            else:
                                return True
        return False


class ViewEventView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(ViewEventView, self).__init__(*args, **kwargs)

        self._eventID = kwargs.get("eventID")
        self._formClass = constants.FORM_MAP.get(self.currentPage)
        self._currentEvent = None

    @property
    def eventID(self):
        return self._eventID

    @property
    def pageContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
            self._pageContext["event"] = self.currentEvent
            self._pageContext["source"] = self.currentPage  #used for manual form, so form source should be current
            self._pageContext["possibleDestinations"] = {"edit": CREATE_EVENT,
                                                         "browse": BROWSE_EVENTS}
            self._pageContext["destination"] = self.destinationPage
        return self._pageContext

    @property
    def currentEvent(self):
        if self._currentEvent is None:
            self._currentEvent = models.Event.objects.get(eventID=self.eventID)
        return self._currentEvent

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
        self._formInitialValues["source"] = self.currentPage
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
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)

