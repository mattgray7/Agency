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


class BrowseEventsView(views.GenericView):
    def __init__(self, *args, **kwargs):
        super(BrowseEventsView, self).__init__(*args, **kwargs)
        self._eventList = None

    @property
    def pageContext(self):
        self._pageContext["events"] = self.eventList
        self._pageContext["browseView"] = BROWSE_EVENTS
        return self._pageContext

    @property
    def eventList(self):
        if self._eventList is None:
            #TODO get 50 or so at a time
            self._eventList = models.Event.objects.all()
        return self._eventList

    def process(self):
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)
