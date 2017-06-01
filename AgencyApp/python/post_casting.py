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
        attributes = {}
        error = False
        if self.request.POST.get("descriptionEnabled", False) in ["False", False]:
            self.record.descriptionEnabled = False
            self.record.save()
        else:
            self.record.descriptionEnabled = True
            self.record.save()
            for formInput in self.request.POST:
                if formInput.startswith("attributes."):
                    splitted = formInput.split(".")
                    attribute = {splitted[1]: self.request.POST.get(formInput)}
                    if self.request.POST.get(formInput) in [True, False, "True", "False", "true", "false"]:
                        try:
                            attributeModel = models.ActorDescriptionBooleanAttribute.objects.get(postID=self.postID,
                                                                                                 attributeName=splitted[1])
                            attributeModel.attributeValue = self.request.POST.get(formInput) in [True, "True", "true"] or False
                        except models.ActorDescriptionBooleanAttribute.DoesNotExist:
                            attributeModel = models.ActorDescriptionBooleanAttribute(postID=self.postID,
                                                                                     attributeName = splitted[1],
                                                                                     attributeValue = bool(self.request.POST.get(formInput)))
                    else:
                        try:
                            attributeModel = models.ActorDescriptionStringAttribute.objects.get(postID=self.postID,
                                                                                                attributeName = splitted[1])
                            attributeModel.attributeValue = self.request.POST.get(formInput)
                        except models.ActorDescriptionStringAttribute.DoesNotExist:
                            attributeModel = models.ActorDescriptionStringAttribute(postID=self.postID,
                                                                                    attributeName = splitted[1],
                                                                                    attributeValue = self.request.POST.get(formInput))
                    attributeModel.save()
        return not error


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

    @property
    def pageContext(self):
        self._pageContext = super(ViewCastingPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"edit": constants.EDIT_POST,
                                                     "createCasting": constants.CREATE_CASTING_POST,
                                                     "createWork": constants.CREATE_WORK_POST,
                                                     "viewCasting": constants.VIEW_POST,
                                                     "viewWork": constants.VIEW_POST}
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


