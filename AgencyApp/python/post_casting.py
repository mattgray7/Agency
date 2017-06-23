import post
import constants
import models
import helpers

import json
from itertools import chain
import actorDescription

class CastingPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.CASTING_POST
        self._projectID = kwargs.get("projectID")
        super(CastingPostInstance, self).__init__(*args, **kwargs)
        self._database = models.CastingPost

    def checkModelFormValues(self):
        return True

    def saveModelFormValues(self):
        if self.record:
            self.record.paid = self.request.POST.get("paid", False) and True  #get value will be 'true' instead of True
            self.record.projectID = self.projectID
            self.record.save()
            return self.saveActorAttributes()
        return False

    def saveActorAttributes(self):
        # Will handle the deletion of objects if disabled
        attributeObject = actorDescription.CastingPostAttributes(request=self.request,
                                                                 postID=self.postID,
                                                                 pageType=constants.CASTING_POST)
        attributeObject.save()
        return True



class CreateCastingPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.CASTING_POST
        super(CreateCastingPostView, self).__init__(*args, **kwargs)
        self._attributeListObject = None

    @property
    def attributeListObject(self):
        if self._attributeListObject is None:
            self._attributeListObject = actorDescription.CastingPostAttributes(request=self.request, postID=self.postID, pageType=constants.CASTING_POST)
        return self._attributeListObject

    @property
    def pageContext(self):
        self._pageContext = super(CreateCastingPostView, self).pageContext
        self._pageContext["attributes"] = self.attributeListObject.attributes
        self._pageContext["descriptionEnabled"] = self.post.record.descriptionEnabled
        self._pageContext["statusOptions"] = constants.CASTING_STATUS_LIST
        self._pageContext["defaultStatus"] = "Open"
        return self._pageContext

    @property
    def post(self):
        if self._post is None:
            self._post = CastingPostInstance(request=self.request, postID=self.postID, projectID=self.projectID, postType=constants.CREATE_CASTING_POST)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateCastingPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["paid"] = self.post.record.paid
            self._formInitialValues["postID"] = self.post.record.postID
            self._formInitialValues["projectID"] = self.projectID
        return self._formInitialValues


class ViewCastingPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewCastingPostView, self).__init__(*args, **kwargs)
        self._attributeListObject = None
        self._castingRole = None
        self._actor = None
        self._displayStatus = None  #current or past

    @property
    def displayStatus(self):
        if self._displayStatus is None:
            projectStatus = self.project.record and self.project.record.status or None
            if projectStatus in ["Pre-production", "In production", "Post production", "Screening"]:
                self._displayStatus = "current"
            elif projectStatus in ["Completed"]:
                self._displayStatus = "past"
        return self._displayStatus

    @property
    def castingRole(self):
        if self._castingRole is None:
            try:
                self._castingRole = models.ProjectRole.objects.get(postID=self.postID)
            except models.ProjectRole.DoesNotExist:
                pass
        return self._castingRole

    @property
    def actor(self):
        if self._actor is None:
            if self.post.record.status == "Cast" and self.castingRole:
                try:
                    self._actor = models.UserAccount.objects.get(username=self.castingRole.username)
                except models.UserAccount.DoesNotExist:
                    pass
        return self._actor

    @property
    def pageContext(self):
        self._pageContext = super(ViewCastingPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"edit": constants.EDIT_POST,
                                                     "createCasting": constants.CREATE_CASTING_POST,
                                                     "createWork": constants.CREATE_WORK_POST,
                                                     "viewCasting": constants.VIEW_POST,
                                                     "viewWork": constants.VIEW_POST}
        self._pageContext["castingRole"] = self.castingRole
        self._pageContext["actor"] = self.actor
        self._pageContext["displayStatus"] = self.displayStatus
        if self.attributeListObject.attributes:
            self._pageContext["attributes"] = self.attributeListObject.attributes
            self._pageContext["descriptionEnabled"] = self.post.record.descriptionEnabled
        return self._pageContext

    @property
    def attributeListObject(self):
        if self._attributeListObject is None:
            self._attributeListObject = actorDescription.CastingPostAttributes(request=self.request, postID=self.postID, pageType=constants.CASTING_POST)
        return self._attributeListObject

    @property
    def post(self):
        if self._post is None:
            # Cant pass projectID as it will lead to infinite loop
            self._post = CastingPostInstance(request=self.request, postID=self.postID, postType=constants.CASTING_POST)
        return self._post

    def createProjectChild(self):
        try:
            newRole = models.ProjectRole.objects.get(postID=self.postID, projectID=self.projectID)
        except models.ProjectRole.DoesNotExist:
            newRole = models.ProjectRole(postID=self.postID, projectID=self.projectID, status="Open")
            newRole.save()
