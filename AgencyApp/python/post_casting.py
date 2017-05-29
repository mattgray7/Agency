import post
import constants
import models
import helpers

import json
from itertools import chain

class CastingPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.CASTING_POST
        self._projectID = kwargs.get("projectID")
        super(CastingPostInstance, self).__init__(*args, **kwargs)
        self._database = models.CastingPost

    @property
    def projectID(self):
        """The project associated with the role being cast"""
        if self._projectID is None:
            if post.isProjectPost(self.postID):
                self._projectID = self.postID
            else:
                self._projectID = self.request.POST.get("projectID") or helpers.getMessageFromKey(self.request, "projectID")
                if not post.isProjectPost(self._projectID):
                    self._projectID = None
        return self._projectID

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
        if self.request.POST.get("descriptionEnabled", "False") == "False":
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
        self._attributes = None
        super(CreateCastingPostView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext = super(CreateCastingPostView, self).pageContext
        self._pageContext["attributes"] = self.attributes
        self._pageContext["descriptionEnabled"] = self.post.record.descriptionEnabled
        return self._pageContext

    @property
    def attributes(self):
        if self._attributes is None:
            if models.CastingPost.objects.get(postID=self.postID).descriptionEnabled:
                self._attributes = getSelectedCastingAttributeValues(self.postID)
            else:
                self._attributes = constants.ACTOR_ATTRIBUTE_DICT
        return self._attributes

    @property
    def post(self):
        if self._post is None:
            self._post = CastingPostInstance(request=self.request, postID=self.postID, projectID=self.projectID)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateCastingPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["paid"] = self.post.record.paid
            self._formInitialValues["postID"] = self.post.record.postID
            self._formInitialValues["projectID"] = self.projectID
            self._formInitialValues["status"] = self.post.record.status
        return self._formInitialValues


class ViewCastingPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        self._attributes = None
        super(ViewCastingPostView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext = super(ViewCastingPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"edit": constants.EDIT_POST,
                                                     "createCasting": constants.CREATE_CASTING_POST,
                                                     "createWork": constants.CREATE_WORK_POST,
                                                     "viewCasting": constants.VIEW_POST,
                                                     "viewWork": constants.VIEW_POST}
        if self.attributes:
            self._pageContext["attributes"] = self.attributes
        return self._pageContext

    @property
    def attributes(self):
        if self._attributes is None:
            if models.CastingPost.objects.get(postID=self.postID).descriptionEnabled:
                self._attributes = getSelectedCastingAttributeValues(self.postID)
        return self._attributes

    @property
    def post(self):
        if self._post is None:
            self._post = CastingPostInstance(request=self.request, postID=self.postID, projectID=self.projectID, postType=constants.CASTING_POST)
        return self._post


def getSelectedActorAttributeValues(username=None):
    """ Returns the default values of constants.ACTOR_ATTRIBUTE_DICT with any selected values changed"""
    selectedAttributes = []
    for attribute in sorted(chain(models.ActorDescriptionStringAttribute.objects.filter(username=username),
                                  models.ActorDescriptionBooleanAttribute.objects.filter(username=username))):
        selectedAttributes.append({"name": attribute.attributeName, "value": attribute.attributeValue})
    return _getAttributeDict(selectedAttributes)


def getSelectedCastingAttributeValues(postID):
    if models.CastingPost.objects.get(postID=postID).descriptionEnabled:
        selectedAttributes = []
        for attribute in sorted(chain(models.ActorDescriptionStringAttribute.objects.filter(postID=postID),
                                      models.ActorDescriptionBooleanAttribute.objects.filter(postID=postID))):
            selectedAttributes.append({"name": attribute.attributeName, "value": attribute.attributeValue})
        return _getAttributeDict(selectedAttributes)
    else:
        return constants.ACTOR_ATTRIBUTE_DICT


def _getAttributeDict(selectedAttributes):
    attributeDict = constants.ACTOR_ATTRIBUTE_DICT
    for attribute in attributeDict:
        for selectedAttribute in selectedAttributes:
            if attribute.get("name") == selectedAttribute.get("name") and attribute.get("value") != selectedAttribute.get("value"):
                attribute["value"] = selectedAttribute.get("value")
    return attributeDict


