from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import models
import helpers
import constants
import views
import string, random
import json


class CreatePostMainView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreatePostMainView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext["possibleSources"] = {"login": constants.LOGIN,
                                                "home": constants.HOME,
                                                "createAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH,
                                                "setupProfileFinish": constants.SETUP_ACCOUNT_FINISH
                                                }
        self._pageContext["possibleDestinations"] = {"collaboration": constants.CREATE_COLLABORATION_POST,
                                                     "project": constants.CREATE_PROJECT
                                                     }
        return self._pageContext


class CreateProjectView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        super(CreateProjectView, self).__init__(*args, **kwargs)
        self._formClass = constants.FORM_MAP.get(self.currentPage)
        self._projectID = None
        self._currentProject = None

        self._pictureModel = self.currentProject
        self._pictureModelFieldName = "projectPicture"

    @property
    def projectID(self):
        if self._projectID is None:
            self_projectID = helpers.createUniqueID(destDatabase=models.Project, idKey="projectID")
        return self._projectID

    @property
    def currentProject(self):
        if self._currentProject is None:
            try:
                self._currentProject = models.Project.objects.get(projectID=self.projectID)
            except models.Project.DoesNotExist:
                pass
        return self._currentProject

    @property
    def pageContext(self):
        self._pageContext["possibleSources"] = {"login": constants.LOGIN,
                                                "home": constants.HOME,
                                                "createAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH,
                                                "setupProfileFinish": constants.SETUP_ACCOUNT_FINISH
                                                }
        self._pageContext["possibleDestinations"] = {"collaboration": constants.CREATE_COLLABORATION_POST}
        return self._pageContext


class GenericCreatePostView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        super(GenericCreatePostView, self).__init__(*args, **kwargs)
        self._formClass = constants.FORM_MAP.get(self.currentPage)
        self._postID = None
        self._currentPost = None
        self._pictureModel = None
        self._pictureModelFieldName = "postPicture"

    @property
    def postID(self):
        if self._postID is None:
            self_postID = helpers.createUniqueID(destDatabase=models.Post, idKey="postID")
        return self._postID

    @property
    def currentPost(self):
        """To be overridden in child class"""
        return None

    @property
    def pictureModel(self):
        """To be overridden in child class"""
        return self.currentPost


class CreateCollaborationPostView(GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        super(CreateCollaborationPostView, self).__init__(*args, **kwargs)

    @property
    def currentPost(self):
        if self._currentPost is None:
            try:
                self._currentPost = models.CollaborationPost.objects.get(postID=self.postID)
            except models.CollaborationPost.DoesNotExist:
                pass
        return self._currentPost

    """@property
    def pageContext(self):
        self._pageContext["possibleSources"] = {"createPost": constants.CREATE_POST}
        self._pageContext["possibleDestinations"] = {"collaboration": constants.CREATE_COLLABORATION_POST}
        return self._pageContext"""

class CreateWorkPostView(GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        super(CreateWorkPostView, self).__init__(*args, **kwargs)

    @property
    def currentPost(self):
        if self._currentPost is None:
            try:
                self._currentPost = models.WorkPost.objects.get(postID=self.postID)
            except models.WorkPost.DoesNotExist:
                pass
        return self._currentPost

