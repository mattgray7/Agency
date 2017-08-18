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
        self.formSubmitted = kwargs.get("formSubmitted", False)
        self._postID = kwargs.get("postID")
        self._postType = kwargs.get("postType")
        self._projectID = kwargs.get("projectID")
        self._record = None
        self._database = None
        self._formErrors = None
        self._errors = []

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID") or helpers.getMessageFromKey(self.request,
                                                                                        "postID")
        return self._postID

    @property
    def projectID(self):
        if self._projectID is None:
            self._projectID = self.request.POST.get("projectID") or helpers.getMessageFromKey(self.request,
                                                                                              "ptojectID")
            if self._projectID is None:
                if self.record.projectID:
                    self._projectID = self.record.projectID
        return self._projectID
    @property
    def record(self):
        if self._record is None:
            try:
                self._record = self.database.objects.get(postID=self.postID)
            except self.database.DoesNotExist:
                if self.formSubmitted:
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
            self.record.status = self.request.POST.get("status", "")
            if self.request.FILES.get("postPicture"):
                self._record.postPicture = self.request.FILES.get("postPicture")
            self.record.save()
            return True
        return False

    def saveModelFormValues(self):
        """To be overridden in child class"""
        return True

    def createPostAdmin(self):
        try:
            currentAdmin = models.PostAdmin.objects.get(username=self.request.user.username, postID=self.postID)
        except models.PostAdmin.DoesNotExist:
            newAdmin = models.PostAdmin(username=self.request.user.username, postID=self.postID)
            newAdmin.save()

    def formIsValid(self):
        if self.request.POST:
            if self.checkBasicFormValues() and self.checkModelFormValues():
                if not self.formErrors:
                    if self.saveBasicFormValues() and self.saveModelFormValues():
                        self.createPostAdmin()
                        return True
        return False

    def _checkTitle(self, title):
        if len(title) < 1:
            self._errors.append("Title must be at least 30 characters long.")
            return False
        return True

    def _checkPoster(self, poster):
        if poster != self.request.user.username:
            self._errors.append("You must be logged in to create an post.")
            return False
        return True

    def _checkDescription(self, description):
        if len(description) < 1:  #TODO switch min length
            self._errors.append("Post description must be at least 75 characters long.")
            return False
        return True

    @property
    def formErrors(self):
        if not self._formErrors:
            self._formErrors = {}

            # Dirty hack to get current page from post type
            currentPage = "CREATE_{0}".format(self.postType)
            formClass = constants.FORM_MAP.get(currentPage)
            form = formClass(self.request.POST)
            if not form.is_valid():
                errorDict = {}
                for field in form:
                    if field.errors:
                        errorMessage = str(field.errors).replace('<ul class="errorlist"><li>', '').replace('</li></ul>', '')
                        if errorMessage in errorDict:
                            errorDict[errorMessage].append(field.label.replace("*", ""))
                        else:
                            errorDict[errorMessage] = [field.label.replace("*", "")]

                # Add more error messages here when they occur and should be stopped
                self._formErrors["required"] =  errorDict["This field is required."]
        return self._formErrors

    @property
    def errors(self):
        return self._errors



class GenericCreatePostView(views.PictureFormView):
    def __init__(self, *args, **kwargs):
        self._postID = kwargs.get("postID")
        self._projectID = None
        self._project = None
        self._postType = kwargs.get("postType")
        self._post = None
        super(GenericCreatePostView, self).__init__(*args, **kwargs)
        self._pictureModel = None
        self._pictureModelFieldName = "postPicture"
        self._currentPageURL = None
        self._roleSelectFields = None
        self._jobSelectFields = None
        self._projectSelectFields = None


    @property
    def projectID(self):
        if self._projectID is None:
            if self._post and self._post.record and self._post.record.projectID:
                self._projectID = self.post.record.projectID
            else:
                self._projectID = self.request.POST.get("projectID", helpers.getMessageFromKey(self.request, "projectID"))
        return self._projectID

    @property
    def project(self):
        if self._project is None:
            if self.projectID:
                self._project = projectPost.ProjectPostInstance(request=self.request, postID=self.projectID, postType=constants.PROJECT_POST)
        return self._project

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID")
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

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.sourcePage
        return self._cancelSource

    def cancelPage(self):
        super(GenericCreatePostView, self).cancelPage()
        if self.request.POST.get(constants.CANCEL) == "True" and self.post.record and not self.post.record.title:
            self.post.database.objects.filter(postID=self.postID).delete()

    @property
    def formSubmitted(self):
        if self.currentPage == constants.EDIT_POST or (isPostPage(self.currentPage) and self.currentPage != constants.VIEW_POST):
            if self.sourcePage == constants.EDIT_POST or (isPostPage(self.sourcePage) and self.sourcePage != constants.VIEW_POST):
                self._formSubmitted = True
            else:
                self._formSubmitted = self.sourcePage == self.currentPage
        else:
            self._formSubmitted = self.sourcePage == self.currentPage
        return self._formSubmitted

    @property
    def roleSelectFields(self):
        if self._roleSelectFields is None:
            self._roleSelectFields = {"names": [], "options": {}, "defaults": {}}
            for field in constants.ACTOR_ATTRIBUTE_DICT:
                if field.get("options"):
                    name = field.get("name")
                    if name:
                        self._roleSelectFields["names"].append(name)
                        if field.get("options"):
                            self._roleSelectFields["options"][name] = field.get("options")
                        if self.formInitialValues.get(name):
                            self._roleSelectFields["defaults"][name] = self.formInitialValues.get(name)
                        elif field.get("value"):
                            self._roleSelectFields["defaults"][name] = "-"
        return self._roleSelectFields

    @property
    def jobSelectFields(self):
        if self._jobSelectFields is None:
            professionList = []
            for section in constants.PROFESSIONS:
                professionList += constants.PROFESSIONS[section]
            self._jobSelectFields = {"names": ["profession"], "options": {"profession": sorted(professionList)}, "defaults": {"profession": "-"}}
        return self._jobSelectFields

    @property
    def projectSelectFields(self):
        if self._projectSelectFields is None:
            self._projectSelectFields = {"names": ["projectType"], "options": {"projectType": constants.PROJECT_TYPE_LIST}, "defaults": {"projectType": "-"}}
        return self._projectSelectFields

    @property
    def pageContext(self):
        self._pageContext["post"] = self.post.record
        self._pageContext["project"] = self.project and self.project.record
        self._pageContext["projectID"] = self.projectID
        self._pageContext["hideStatus"] = False
        self._pageContext["postType"] = self.post.postType
        self._pageContext["possibleDestinations"] = {"viewPost": constants.VIEW_POST}
        self._pageContext["selectFields"] = {"roles": self.roleSelectFields,
                                             "jobs": self.jobSelectFields,
                                             "projects": self.projectSelectFields}
        self._pageContext['statusOptions'] = {"roles": constants.CASTING_STATUS_LIST,
                                              "jobs": constants.WORK_STATUS_LIST,
                                              "events": constants.EVENT_STATUS_LIST,
                                              "projects": constants.PROJECT_STATUS_LIST}
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
            self._cancelButtonExtraInputs = super(GenericCreatePostView, self).cancelButtonExtraInputs or {}
        self._cancelButtonExtraInputs["postID"] = self.postID
        self._cancelButtonExtraInputs["projectID"] = self.projectID
        if self.projectID and not self.post:
            # Cancel back to project if canceling a new post and the poroject exists
            self._cancelButtonExtraInputs["skipToProject"] = True
        return self._cancelButtonExtraInputs

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
    def currentPageURL(self):
        if self._currentPageURL is None:
            self._currentPageURL = constants.URL_MAP.get(self.currentPage).format(self.postID)
        return self._currentPageURL

    @property
    def formInitialValues(self):
        self._formInitialValues["postID"] = self.postID
        self._formInitialValues["projectID"] = self.projectID
        self._formInitialValues["poster"] = self.username
        if self.post.record:
            self._formInitialValues["title"] = self.post.record.title
            self._formInitialValues["description"] = self.post.record.description
            self._formInitialValues["status"] = self.post.record.status
        return self._formInitialValues

    def updateSourcePicture(self, tempID):
        """ Updates the sourcePicture property of the PictureFormView class to use the temp picture 
        instead of the picture from request.FILES
        """
        try:
            tempPicture = models.TempPostPicture.objects.get(tempID=tempID)
        except models.TempPostPicture.DoesNotExist:
            print "No temp picture found with ID {0}".format(tempID)
            pass
        else:
            if tempPicture.postPicture:
                self._sourcePicture = tempPicture.postPicture
                return True
        return False

    def processForm(self):
        # If a temp picture ID exists in the request, update the source picture for the form to use the temp pic
        tempPostPictureID = self.request.POST.get("tempPostPictureID")
        if tempPostPictureID:
            self.updateSourcePicture(tempPostPictureID)
        return self.post.formIsValid()


class GenericViewPostView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._postID = kwargs.get("postID")
        self._projectID = None
        self._project = None
        self._post = None
        self._postType = None
        super(GenericViewPostView, self).__init__(*args, **kwargs)
        self._isProjectAdmin = False
        self._isPostAdmin = False
        self._projectDisplayStatus = None

    @property
    def projectDisplayStatus(self):
        if self._projectDisplayStatus is None:
            projectStatus = self.project and self.project.record and self.project.record.status or None
            if projectStatus in ["Pre-production", "In production", "Post production", "Screening"]:
                self._projectDisplayStatus = "current"
            elif projectStatus in ["Completed"]:
                self._projectDisplayStatus = "past"
        return self._projectDisplayStatus

    @property
    def isPostAdmin(self):
        if self._isPostAdmin is False:
            postAdmins = models.PostAdmin.objects.filter(postID=self.postID)
            for admin in postAdmins:
                if admin.username == self.request.user.username:
                    self._isPostAdmin = True
        return self._isPostAdmin

    @property
    def isProjectAdmin(self):
        if self._isProjectAdmin is False:
            projectAdmins = models.ProjectAdmin.objects.filter(projectID=self.projectID)
            for admin in projectAdmins:
                if admin.username == self.request.user.username:
                    self._isProjectAdmin = True
        return self._isProjectAdmin

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.get("postID") or helpers.getMessageFromKey(self.request, "postID")
        return self._postID

    @property
    def projectID(self):
        if self._projectID is None:
            self._projectID = self.request.POST.get("projectID", helpers.getMessageFromKey(self.request, "projectID"))
            if self._projectID is None:
                if self.post.record and self.post.record.projectID:
                    self._projectID = self.post.record.projectID
        return self._projectID

    @property
    def project(self):
        if self._project is None:
            if self.projectID:
                self._project = projectPost.ProjectPostInstance(request=self.request, postID=self.projectID, postType=constants.PROJECT_POST)
        return self._project

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
    def currentPageURL(self):
        if self._currentPageURL is None:
            self._currentPageURL = constants.URL_MAP.get(self.currentPage).format(self.postID)
        return self._currentPageURL

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
            self._cancelDestinationURL = constants.URL_MAP.get(self.currentPage)
            if self.postID and self._cancelDestinationURL:
                self._cancelDestinationURL = self._cancelDestinationURL.format(self.postID)
        return self._cancelDestinationURL

    @property
    def cancelButtonExtraInputs(self):
        self._cancelButtonExtraInputs = super(GenericViewPostView, self).cancelButtonExtraInputs
        self._cancelButtonExtraInputs["postID"] = self.postID
        self._cancelButtonExtraInputs["projectID"] = self.projectID
        return self._cancelButtonExtraInputs

    @property
    def cancelDestination(self):
        if self._cancelDestination is None:
            self._cancelDestination = constants.BROWSE_POST_PAGE_MAP.get(self.post and self.post.postType or constants.PROFILE)
        return self._cancelDestination

    @property
    def pageContext(self):
        self._pageContext["post"] = self.postID and self.post.record or None
        self._pageContext["possibleSources"] = {"profile": constants.PROFILE}
        self._pageContext["possibleDestinations"] = {"editPost": constants.EDIT_POST,
                                                     "profile": constants.PROFILE,
                                                     "viewPost": constants.VIEW_POST,
                                                     "browse": {"events": constants.BROWSE_EVENTS,
                                                                "projects": constants.BROWSE_PROJECTS,
                                                                "users": constants.BROWSE_USERS,
                                                                "posts": constants.BROWSE_POSTS}}
        self._pageContext["isEvent"] = isEventPost(self.postID)
        self._pageContext["isProject"] = isProjectPost(self.postID)
        self._pageContext["isCollaboration"] = isCollaborationPost(self.postID)
        self._pageContext["isWork"] = isWorkPost(self.postID)
        self._pageContext["isCasting"] = isCastingPost(self.postID)
        self._pageContext["userIsAdmin"] = self.isPostAdmin
        self._pageContext["displayStatus"] = self.projectDisplayStatus
        self._pageContext['statusOptions'] = {"roles": constants.CASTING_STATUS_LIST,
                                              "jobs": constants.WORK_STATUS_LIST,
                                              "events": constants.EVENT_STATUS_LIST,
                                              "projects": constants.PROJECT_STATUS_LIST}
        if self.projectID:
            self._pageContext["projectID"] = self.projectID
        self._pageContext["project"] = self.project
        self._pageContext["following"] = isFollowingPost(self.postID, self.request.user.username)
        return self._pageContext

    def createProjectChild(self):
        """ To be overridden in child class, will create a ProjectRole or ProjectJob for ex"""
        pass

    def processForm(self):
        success = False
        if self.request.POST.get("setProject") == "True":
            if self.request.POST.get("projectID"):
                try:
                    self.post.record.projectID = self.request.POST.get("projectID")
                    self.post.record.save()
                except Exception as e:
                    print "Error adding casting post to project: {0}".format(e)
                else:
                    self.createProjectChild()
                    success = True
        else:
            success = True
        return success

# ================================================================================================== #

import post_project as projectPost

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

def getPost(postID):
    database = getPostDatabase(postID)
    post = None;
    if database:
        try:
            post = database.objects.get(postID=postID)
        except database.DoesNotExist:
            pass
    return post

def getPostDatabase(postID):
    database = None
    if isEventPost(postID):
        database = models.EventPost
    elif isProjectPost(postID):
        database = models.ProjectPost
    elif isCollaborationPost(postID):
        database = models.CollaborationPost
    elif isWorkPost(postID):
        database = models.WorkPost
    elif isCastingPost(postID):
        database = models.CastingPost
    return database

def getPostInstanceClass(postID):
    import post_casting as castingPost
    import post_work as workPost
    import post_event as eventPost
    import post_project as projectPost
    instance = None
    if isEventPost(postID):
        instance = eventPost.EventPostInstance
    elif isProjectPost(postID):
        instance = projectPost.ProjectPostInstance
    elif isWorkPost(postID):
        instance = workPost.WorkPostInstance
    elif isCastingPost(postID):
        instance = castingPost.CastingPostInstance
    return instance

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

