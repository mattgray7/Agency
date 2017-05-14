from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict

# Create your views here.
from django.http import HttpResponseRedirect

from constants import *
import constants
import helpers
import views
import models

import json


class BrowseView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(BrowseView, self).__init__(*args, **kwargs)
        self._eventList = None
        self._projectList = None
        self._collabPostList = None
        self._workPostList = None
        self._castingPostList = None

    @property
    def pageContext(self):
        self._pageContext["possibleViews"] = {"event": constants.BROWSE_EVENTS,
                                              "project": constants.BROWSE_PROJECTS,
                                              "collabPost": constants.BROWSE_COLLABORATION_POSTS,
                                              "workPost": constants.BROWSE_WORK_POSTS,
                                              "castingPost": constants.BROWSE_CASTING_POSTS,
                                              "post": constants.BROWSE_POSTS,
                                              "browse": constants.BROWSE}
        self._pageContext["possibleDestinations"] = {"viewPost": constants.VIEW_POST}

        # TODO don't load everything if for /browse/events/ for example (can load the others through ajax)
        self._pageContext["events"] = self.eventList
        self._pageContext["projects"] = self.projectList
        self._pageContext["collabPosts"] = self.collabPostList
        self._pageContext["workPosts"] = self.workPostList
        self._pageContext["castingPosts"] = self.castingPostList
        self._pageContext["browseView"] = self.currentPage
        return self._pageContext

    @property
    def eventList(self):
        if self._eventList is None:
            #TODO get 50 or so at a time
            self._eventList = models.EventPost.objects.all()
        return self._eventList

    @property
    def projectList(self):
        if self._projectList is None:
            self._projectList = models.ProjectPost.objects.all()
        return self._projectList

    @property
    def collabPostList(self):
        if self._collabPostList is None:
            self._collabPostList = models.CollaborationPost.objects.all()
        return self._collabPostList

    @property
    def workPostList(self):
        if self._workPostList is None:
            self._workPostList = models.WorkPost.objects.all()
        return self._workPostList

    @property
    def castingPostList(self):
        if self._castingPostList is None:
            self._castingPostList = models.CastingPost.objects.all()
        return self._castingPostList

def isBrowsePage(pageName):
    return pageName in [constants.BROWSE, constants.BROWSE_EVENTS, constants.BROWSE_PROJECTS,
                        constants.BROWSE_POSTS, constants.BROWSE_COLLABORATION_POSTS,
                        constants.BROWSE_WORK_POSTS, constants.BROWSE_CASTING_POSTS]