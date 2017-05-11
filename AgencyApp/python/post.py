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

# =================== INSTANCES ====================== #
class PostInstance(object):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        self._postID = kwargs.get('postID')
        self._record = None
        self._database = None
        self._postTypePageName = None

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID")
            if self._postID is None:
                self._postID = helpers.createUniqueID(destDatabase=self.database, idKey="postID")
        return self._postID

    @property
    def record(self):
        if self._record is None:
            try:
                self._record = self.database.objects.get(postID=self.postID)
            except self.database.DoesNotExist:
                self._record = self.database(postID=self.postID,
                                             poster=self.request.user.username)
                self._record.save()
        return self._record

    @property
    def database(self):
        """To be overridden in child class"""
        return self.database

    @property
    def postTypePageName(self):
        """To be overridden in child class"""
        return self._postTypePageName


class CollaborationPostInstance(PostInstance):
    def __init__(self, *args, **kwargs):
        super(CollaborationPostInstance, self).__init__(*args, **kwargs)

    @property
    def database(self):
        if self._database is None:
            self._database = models.CollaborationPost
        return self._database

    @property
    def postTypePageName(self):
        if self._postTypePageName is None:
            self._postTypePageName = constants.CREATE_COLLABORATION_POST
        return self._postTypePageName


class WorkPostInstance(PostInstance):
    def __init__(self, *args, **kwargs):
        super(WorkPostInstance, self).__init__(*args, **kwargs)

    @property
    def database(self):
        if self._database is None:
            self._database = models.WorkPost
        return self._database

    @property
    def postTypePageName(self):
        if self._postTypePageName is None:
            self._postTypePageName = constants.CREATE_WORK_POST
        return self._postTypePageName

# =================== END OF INSTANCES ====================== #

# ======================= VIEWS ======================== #


class CreatePostMainView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreatePostMainView, self).__init__(*args, **kwargs)

    @property
    def cancelDestination(self):
        return constants.HOME

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
    def cancelButtonName(self):
        return "Back"

    @property
    def cancelDestination(self):
        return constants.CREATE_POST

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
        self._post = None
        self._postID = None
        self._pictureModel = None
        self._pictureModelFieldName = "postPicture"

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID")
        return self._postID

    @property
    def post(self):
        """To be overridden in child class"""
        return self._post

    @property
    def pageContext(self):
        self._pageContext["post"] = self.post.record
        return self._pageContext

    @property
    def filename(self):
        if self._filename is None:
            self._filename = constants.MEDIA_FILE_NAME_MAP.get(self.post.postTypePageName, "tempfile")
            self._filename = self._filename.format(self.postID)
        return self._filename

    @property
    def cancelButtonName(self):
        return "Back"

    @property
    def currentPageHtml(self):
        if self._currentPageHtml is None:
            if self.currentPage == constants.EDIT_EVENT:
                self._currentPageHtml = constants.HTML_MAP.get(self.post.postTypePageName)
            else:
                self._currentPageHtml = constants.HTML_MAP.get(self.currentPage)
        return self._currentPageHtml

    @property
    def formClass(self):
        if self._formClass is None:
            if self.currentPage == constants.EDIT_EVENT:
                self._formClass = constants.FORM_MAP.get(self.post.postTypePageName)
            else:
                self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def pictureModel(self):
        """To be overridden in child class"""
        return self.post.postRecord

    @property
    def formInitialValues(self):
        self._formInitialValues["postID"] = self.postID
        self._formInitialValues["poster"] = self.username
        if self.post.record:
            self._formInitialValues["title"] = self.post.record.title
            self._formInitialValues["description"] = self.post.record.description
            self._formInitialValues["profession"] = self.post.record.profession
        return self._formInitialValues


class CreateCollaborationPostView(GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        super(CreateCollaborationPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if not self.postID:
                self._postID = helpers.createUniqueID(destDatabase=models.CollaborationPost, idKey="postID")
            self._post = CollaborationPostInstance(request=self.request, postID=self.postID)
        return self._post

    @property
    def cancelDestination(self):
        return constants.CREATE_POST


class CreateWorkPostView(GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        super(CreateWorkPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if not self.postID:
                self._postID = helpers.createUniqueID(destDatabase=models.WorkPost, idKey="postID")
            self._post = WorkPostInstance(request=self.request, postID=self.postID)
        return self._post


class ViewPostView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(ViewPostView, self).__init__(*args, **kwargs)
        raise



def isCollaborationPost(postID):
    return len(models.CollaborationPost.objects.filter(postID=postID)) > 0

def isWorkPost(postID):
    return len(models.WorkPost.objects.filter(postID=postID)) > 0

