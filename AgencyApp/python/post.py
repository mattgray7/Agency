from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import models
import helpers
import constants
import genericViews as views
import browse
import string, random
import json

# =================== Simple post views ===================== #

class CreatePostTypesView(views.GenericFormView):
    """Can create all post types"""
    def __init__(self, *args, **kwargs):
        super(CreatePostTypesView, self).__init__(*args, **kwargs)

    @property
    def cancelDestination(self):
        return constants.HOME

    @property
    def pageContext(self):
        self._pageContext["possibleSources"] = {"post": constants.CREATE_POST,
                                                "createAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH,
                                                "setupProfileFinish": constants.SETUP_ACCOUNT_FINISH
                                                }
        self._pageContext["possibleDestinations"] = {"event": constants.CREATE_EVENT_POST,
                                                     "project": constants.CREATE_PROJECT_POST,
                                                     "collaboration": constants.CREATE_COLLABORATION_POST,
                                                     "work": constants.CREATE_WORK_POST,
                                                     "casting": constants.CREATE_CASTING_POST
                                                     }
        return self._pageContext


class CreatePostChoiceView(views.GenericFormView):
    """Can create work, collab, or casting posts"""
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
                                                     "work": constants.CREATE_WORK_POST,
                                                     "casting": constants.CREATE_CASTING_POST
                                                     }
        return self._pageContext

# ============================================================================================ #



# ==================================== Generic post views ==================================== #

class GenericPostInstance(object):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        self._postID = kwargs.get("postID")
        self._postType = kwargs.get("postType")
        self._record = None
        self._database = None
        self.errors = []

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID") or helpers.getMessageFromKey(self.request,
                                                                                        "postID")
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
    def postType(self):
        """To be overridden in child classs"""
        return self._postType

    @property
    def database(self):
        if self._database is None:
            self._database = constants.POST_DATABASE_MAP.get(self.postType)
        return self._database

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
                self._record.postPicture = self.request.FILES.get("postPicture")
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


class GenericCreatePostView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        self._postID = kwargs.get("postID")
        self._postType = kwargs.get("postType")
        self._post = None
        super(GenericCreatePostView, self).__init__(*args, **kwargs)
        self._pictureModel = None
        self._pictureModelFieldName = "postPicture"

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID") or helpers.getMessageFromKey(self.request,
                                                                                        "postID")
            if not self._postID:
                self._postID = helpers.createUniqueID(destDatabase=constants.POST_DATABASE_MAP.get(self.postType),
                                                      idKey="postID")
        return self._postID

    @property
    def post(self):
        """To be overridden in child class"""
        return self._post

    @property
    def postType(self):
        return self._postType

    def cancelPage(self):
        super(GenericCreatePostView, self).cancelPage()
        if self.sourcePage != constants.VIEW_POST:
            self.post.database.objects.filter(postID=self.postID).delete()

    @property
    def pageContext(self):
        self._pageContext["post"] = self.post.record
        self._pageContext["isEvent"] = isEventPost(self.postID)
        self._pageContext["isProject"] = isProjectPost(self.postID)
        self._pageContext["isCollaboration"] = isCollaborationPost(self.postID)
        self._pageContext["isWork"] = isWorkPost(self.postID)
        self._pageContext["isCasting"] = isCastingPost(self.postID)
        return self._pageContext

    @property
    def filename(self):
        if self._filename is None:
            self._filename = constants.MEDIA_FILE_NAME_MAP.get(self.post.postType, "tempfile")
            self._filename = self._filename.format(self.postID)
        return self._filename

    @property
    def cancelDestination(self):
        return self.sourcePage

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
                self._currentPageHtml = constants.HTML_MAP.get(constants.CREATE_POST_PAGE_MAP.get(self.post.postType))
            else:
                self._currentPageHtml = constants.HTML_MAP.get(self.currentPage)
        return self._currentPageHtml

    @property
    def formClass(self):
        if self._formClass is None:
            if self.currentPage == constants.EDIT_POST:
                self._formClass = constants.FORM_MAP.get(constants.CREATE_POST_PAGE_MAP.get(self.post.postType))
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


class GenericViewPostView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._postID = kwargs.get("postID")
        self._post = None
        super(GenericViewPostView, self).__init__(*args, **kwargs)
        self._postType = None

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.get("postID") or helpers.getMessageFromKey(self.request, "postID")
        return self._postID

    @property
    def post(self):
        """ To be overridden in child class """
        return self._post

    @property
    def postType(self):
        """To be overridden in child class"""
        if self._postType is None:
            self._postType = self.post and self.post.postType
        return self._postType

    @property
    def cancelButtonName(self):
        if browse.isBrowsePage(self.sourcePage):
            self._cancelButtonName = "Back to browse"
        else:
            self._cancelButtonName = "View more posts"
        return self._cancelButtonName

    @property
    def cancelDestinationURL(self):
        if self._cancelDestinationURL is None:
            self._cancelDestinationURL = constants.URL_MAP.get(self.cancelDestination)
            if self.sourcePage == constants.PROFILE:
                # format with username in url
                if self._cancelDestinationURL:
                    self._cancelDestinationURL = self._cancelDestinationURL.format(self.postID)
        return self._cancelDestinationURL

    @property
    def cancelButtonExtraInputs(self):
        if not self._cancelButtonExtraInputs:
            self._cancelButtonExtraInputs = {"postID": self.postID}
        return json.dumps(self._cancelButtonExtraInputs)

    @property
    def cancelDestination(self):
        if self._cancelDestination is None:
            self._cancelDestination = constants.BROWSE_POST_PAGE_MAP.get(self.post.postType or constants.PROFILE)
        return self._cancelDestination

    @property
    def pageContext(self):
        self._pageContext["post"] = self.postID and self.post.record or None
        self._pageContext["possibleSources"] = {"profile": constants.PROFILE}
        self._pageContext["possibleDestinations"] = {"edit": constants.EDIT_POST,
                                                     "profile": constants.PROFILE,
                                                     "browse": {"events": constants.BROWSE_EVENTS,
                                                                "projects": constants.BROWSE_PROJECTS,
                                                                "users": constants.BROWSE_USERS,
                                                                "posts": constants.BROWSE_POSTS}}
        self._pageContext["isEvent"] = isEventPost(self.postID)
        self._pageContext["isProject"] = isProjectPost(self.postID)
        self._pageContext["isCollaboration"] = isCollaborationPost(self.postID)
        self._pageContext["isWork"] = isWorkPost(self.postID)
        self._pageContext["isCasting"] = isCastingPost(self.postID)
        self._pageContext["following"] = isFollowingPost(self.postID, self.request.user.username)
        return self._pageContext

# ================================================================================================== #



# ========================================= Post functions =========================================  #

def followPost(postID, username):
    try:
        follow = models.PostFollow(postID=postID, username=username)
        follow.save()
    except Exception as e:
        print "Could not follow post: {0}".format(e)
        return False
    else:
        return True

def unfollowPost(postID, username):
    try:
        models.PostFollow.objects.filter(postID=postID, username=username).delete()
    except Exception as e:
        print "Could not unfollow post: {0}".format(e)
        return False
    else:
        return True

def isFollowingPost(postID, username):
    return len(models.PostFollow.objects.filter(postID=postID, username=username)) > 0

def _postIDExistsInDb(postID, database):
    return len(database.objects.filter(postID=postID)) > 0

def isEventPost(postID):
    return _postIDExistsInDb(postID, models.EventPost)

def isProjectPost(postID):
    return _postIDExistsInDb(postID, models.ProjectPost)

def isCollaborationPost(postID):
    return _postIDExistsInDb(postID, models.CollaborationPost)

def isWorkPost(postID):
    return _postIDExistsInDb(postID, models.WorkPost)

def isCastingPost(postID):
    return _postIDExistsInDb(postID, models.CastingPost)

def isPostPage(pageName):
    return pageName in [constants.VIEW_POST, constants.CREATE_EVENT_POST,
                        constants.CREATE_COLLABORATION_POST, constants.CREATE_WORK_POST,
                        constants.CREATE_PROJECT_POST, constants.EDIT_POST,
                        constants.CREATE_CASTING_POST]

