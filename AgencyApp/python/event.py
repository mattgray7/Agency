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

class CreateEventView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreateEventView, self).__init__(*args, **kwargs)
        self._eventID = kwargs.get('eventID') or self.request.POST.get("eventID")
        self._formClass = constants.FORM_MAP.get(self.currentPage)
        self._currentEvent = None
        self._eventPicture = None

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
        return self._pageContext

    @property
    def sourcePage(self):
        self._sourcePage = self.incomingSource
        return self._sourcePage

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
        print "formClass is {0}, current page is {1}".format(self._formClass, self.currentPage)
        return self._formClass

    @property
    def formSubmitted(self):
        #return self.request.POST.get("title") and self.request.POST.get("description") and self.request.POST.get("location")
        self._formSubmitted = self.sourcePage == self.currentPage
        print "source {0}, current {1}".format(self.sourcePage, self.currentPage)
        return self._formSubmitted

    @property
    def formInitialValues(self):
        self._formInitialValues["eventID"] = self.eventID
        self._formInitialValues["poster"] = self.username
        self._formInitialValues["source"] = CREATE_EVENT
        self._formInitialValues["eventPicture"] = self.eventPicture # TODO add default image
        if self.currentEvent:
            self._formInitialValues["title"] = self.currentEvent.title
            self._formInitialValues["description"] = self.currentEvent.description
            self._formInitialValues["location"] = self.currentEvent.location
            self._formInitialValues["date"] = self.currentEvent.date
        return self._formInitialValues

    @property
    def form(self):
        if not self._form:
            if self.formSubmitted:
                self._form = self.formClass(self.request.POST, self.request.FILES)
            else:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    @property
    def eventPicture(self):
        if self._eventPicture is None:
            print "Hiii\n\n"
            #print self.request.FILES
            self._eventPicture = self.request.FILES.get("eventPicture")
            if self.formSubmitted:
                print "post, {0}, files, {1}".format(self.request.POST, self.request.FILES)
                # Save picture
                #print "event picture is {0}".format(self._eventPicture)
                if self.currentEvent and self._eventPicture:
                    self.currentEvent.eventPicture = self._eventPicture
                    self.currentEvent.save()
                    print "currentEvent is {0}".format(self.currentEvent)

                    # Rename event file
                    print self._eventPicture
                    initialPath = self.currentEvent.eventPicture.path
                    newName = "event_{0}{1}".format(self.eventID, os.path.splitext(initialPath)[-1])
                    newPath = os.path.join(os.path.dirname(initialPath), newName)
                    os.rename(initialPath, newPath)
                    print "initialPath {0}, newPath {1}".format(initialPath, newPath)

                    self.currentEvent.eventPicture.name = os.path.join(self.username, newName)
                    self.currentEvent.save()
                    print "currentEvent is now {0}".format(self.currentEvent)
                    self._eventPicture = self.currentEvent.eventPicture
        return self._eventPicture

    @property
    def currentEvent(self):
        if self._currentEvent is None:
            try:
                self._currentEvent = models.Event.objects.get(eventID=self.eventID)
                print "found current event"
            except models.Event.DoesNotExist:
                self._currentEvent = models.Event(eventID=self.eventID,
                                                  poster=self.request.user.username)
                self._currentEvent.save()
                print "creating new event"
                pass
        print "currentEvent is {0}".format(self._currentEvent)
        return self._currentEvent
        """
    def renameEventPicture(self):
        self.currentEvent.eventPicture = self.request.FILES["eventPicture"]
        self.currentEvent.save()
        print "currentEvent is {0}".format(currentEvent)

        # Rename event file
        initialPath = self.currentEvent.eventPicture.path
        newName = "event_{0}{1}".format(self.eventID, os.path.splitext(initialPath)[-1])
        newPath = os.path.join(os.path.dirname(initialPath), newName)
        os.rename(initialPath, newPath)
        print "initialPath {0}, newPath {1}".format(initialPath, newPath)

        self.currentEvent.eventPicture.name = os.path.join(self.username, newName)
        self.currentEvent.save()
        print "currentEvent is now {0}".format(currentEvent)
        """
    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                formIsValid = False
                if self.request.POST.get("cancel") != "True":
                    if self.formClass:
                        if self.form.is_valid():
                            print "form is valid"
                            print self.form
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
                            self._currentEvent.eventPicture = self.eventPicture
                            """else:
                                # Create new event
                                eventToSave = models.Event(eventID = self.eventID,
                                                           poster=poster,
                                                           title=title,
                                                           location=location,
                                                           description=description,
                                                           date=date,
                                                           eventPicture=self.eventPicture
                                                           )
                                self._currentEvent = eventToSave"""
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
        self._formInitialValues["source"] = constants.VIEW_EVENT
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

