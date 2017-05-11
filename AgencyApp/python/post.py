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
        self.errors = []

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID") or helpers.getMessageFromKey(self.request,
                                                                                        "postID")
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
        return self._database

    @property
    def postTypePageName(self):
        """To be overridden in child class"""
        return self._postTypePageName

    def checkBasicFormValues(self):
        return (self._checkTitle(title=self.request.POST.get("title", "")) and
                self._checkPoster(poster=self.request.POST.get("poster", "")) and
                self._checkDescription(description=self.request.POST.get("description", "")))

    def checkModelFormValues(self):
        """To be overridden in child class"""
        return True

    def saveBasicFormValues(self):
        """To be overridden in child class"""
        if self.record:
            self.record.title = self.request.POST.get("title", "")
            self.record.poster = self.request.POST.get("poster", "")
            self.record.description = self.request.POST.get("description", "")
            if self.request.FILES.get("postPicture"):
                self.record.postPicture = self.request.FILES.get("postPicture")
            self.record.save()
            return True
        return False

    def saveModelFormValues(self):
        """To be overridden in child class"""
        return True

    def formIsValid(self):
        if self.request.POST:
            if self.checkBasicFormValues() and self.checkModelFormValues():
                return self.saveBasicFormValues() and self.saveModelFormValues()
        return False

    def _checkTitle(self, title):
        if len(title) < 1:
            self.errors.append("Title must be at least 30 characters long.")
            return False
        return True

    def _checkPoster(self, poster):
        if poster != self.request.user.username:
            self.errors.append("You must be logged in to create an post.")
            return False
        return True

    def _checkDescription(self, description):
        if len(description) < 1:  #TODO switch min length
            self.errors.append("Post description must be at least 75 characters long.")
            return False
        return True
               

class ProjectPostInstance(PostInstance):
    def __init__(self, *args, **kwargs):
        super(ProjectPostInstance, self).__init__(*args, **kwargs)
        self._postTypePageName = constants.CREATE_PROJECT_POST
        self._database = models.ProjectPost

    def checkModelFormValues(self):
        """TODO, only thing so far is status, which is optional, so return True"""
        return True

    def saveModelFormValues(self):
        if self.record:
            self.record.status = self.request.POST.get("status", "")
            self.record.save()
            return True
        return False


class CollaborationPostInstance(PostInstance):
    def __init__(self, *args, **kwargs):
        super(CollaborationPostInstance, self).__init__(*args, **kwargs)
        self._postTypePageName = constants.CREATE_COLLABORATION_POST
        self._database = models.CollaborationPost

    def checkModelFormValues(self):
        valid = False
        if self.request.method == "POST":
            if len(self.request.POST.get("profession", "")) < 1:
                self.errors.append("Missing profession")
            else:
                valid = True
        return valid

    def saveModelFormValues(self):
        if self.record:
            self.record.profession = self.request.POST.get("profession", "")
            self.record.save()
            return True
        return False


class WorkPostInstance(PostInstance):
    def __init__(self, *args, **kwargs):
        super(WorkPostInstance, self).__init__(*args, **kwargs)
        self._postTypePageName = constants.CREATE_WORK_POST
        self._database = models.WorkPost

    def checkModelFormValues(self):
        valid = False
        if self.request.method == "POST":
            if len(self.request.POST.get("profession", "")) < 1:
                self.errors.append("Missing profession")
            else:
                valid = True
        return valid

    def saveModelFormValues(self):
        if self.record:
            self.record.profession = self.request.POST.get("profession")
            self.record.paid = self.request.POST.get("paid", False)
            self.record.save()
            return True
        return False

# =================== END OF INSTANCES ====================== #



# ======================= VIEWS ======================== #

class CreatePostChoiceView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(CreatePostChoiceView, self).__init__(*args, **kwargs)

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
                                                     "project": constants.CREATE_PROJECT_POST
                                                     }
        return self._pageContext


class GenericCreatePostView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        self._postID = kwargs.get("postID")
        super(GenericCreatePostView, self).__init__(*args, **kwargs)
        self._post = None
        self._pictureModel = None
        self._pictureModelFieldName = "postPicture"

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID") or helpers.getMessageFromKey(self.request,
                                                                                        "postID")
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
        if self.sourcePage == constants.VIEW_POST:
            return "Cancel"
        else:
            return "Back"

    @property
    def cancelDestinationURL(self):
        if self._cancelDestinationURL is None:
            self._cancelDestinationURL = constants.URL_MAP.get(self.currentPage)
            if self._cancelDestinationURL:
                self._cancelDestinationURL = self._cancelDestinationURL.format(self.postID)
        return self._cancelDestinationURL

    @property
    def cancelButtonExtraInputs(self):
        if not self._cancelButtonExtraInputs:
            self._cancelButtonExtraInputs = {"postID": self.postID}
        return json.dumps(self._cancelButtonExtraInputs)

    @property
    def currentPageHtml(self):
        if self._currentPageHtml is None:
            if self.currentPage == constants.EDIT_POST:
                self._currentPageHtml = constants.HTML_MAP.get(self.post.postTypePageName)
            else:
                self._currentPageHtml = constants.HTML_MAP.get(self.currentPage)
        return self._currentPageHtml

    @property
    def formClass(self):
        if self._formClass is None:
            if self.currentPage == constants.EDIT_POST:
                self._formClass = constants.FORM_MAP.get(self.post.postTypePageName)
            else:
                self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def pictureModel(self):
        """To be overridden in child class"""
        return self.post.record

    @property
    def formInitialValues(self):
        self._formInitialValues["postID"] = self.postID
        self._formInitialValues["poster"] = self.username
        if self.post.record:
            self._formInitialValues["title"] = self.post.record.title
            self._formInitialValues["description"] = self.post.record.description
        return self._formInitialValues

    def processForm(self):
        return self.post.formIsValid()


class CreateProjectPostView(GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        super(CreateProjectPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if not self.postID:
                self._postID = helpers.createUniqueID(destDatabase=models.ProjectPost, idKey="postID")
            self._post = ProjectPostInstance(request=self.request, postID=self.postID)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateProjectPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["status"] = self.post.record.status
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
    def formInitialValues(self):
        self._formInitialValues = super(CreateCollaborationPostView, self).formInitialValues
        self._formInitialValues["postID"] = self.postID
        if self.post.record:
            self._formInitialValues["profession"] = self.post.record.profession
        return self._formInitialValues


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

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateWorkPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["profession"] = self.post.record.profession
            self._formInitialValues["paid"] = self.post.record.paid
        return self._formInitialValues


class ViewPostView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._postID = kwargs.get("postID")
        super(ViewPostView, self).__init__(*args, **kwargs)
        self._post = None

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.get("postID")
        return self._postID

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                if isCollaborationPost(self.postID):
                    self._post = CollaborationPostInstance(request=self.request, postID=self.postID)
                elif isWorkPost(self.postID):
                    self._post = WorkPostInstance(request=self.request, postID=self.postID)
        return self._post

    @property
    def pageContext(self):
        self._pageContext["post"] = self.postID and self.post.record or None
        self._pageContext["possibleDestinations"] = {"edit": constants.EDIT_POST}
        return self._pageContext


def isCollaborationPost(postID):
    return len(models.CollaborationPost.objects.filter(postID=postID)) > 0

def isWorkPost(postID):
    return len(models.WorkPost.objects.filter(postID=postID)) > 0

