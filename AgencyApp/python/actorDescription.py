import models
import constants
import post
from itertools import chain

class ActorAttributes(object):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request");
        self.pageType = kwargs.get("pageType")
        self._selectedAttributes = None
        self._attributes = None
        self._descriptionEnabled = False
        self._descriptionList = None

    @property
    def descriptionList(self):
        """To be overridden in child class"""
        return self._descriptionList        

    @property
    def descriptionEnabled(self):
        """To be overridden in child class"""
        return self._descriptionEnabled

    @property
    def selectedAttributes(self):
        if self._selectedAttributes is None:
            self._selectedAttributes = []
            for attribute in self.descriptionList:
                self._selectedAttributes.append({"name": attribute.attributeName, "value": attribute.attributeValue})
        return self._selectedAttributes

    @property
    def attributes(self):
        if self._attributes is None:
            attributeDict = constants.ACTOR_ATTRIBUTE_DICT
            if self.selectedAttributes and len(self.selectedAttributes) > 0:
                for attribute in attributeDict:
                    for selectedAttribute in self.selectedAttributes:
                        if attribute.get("name") == selectedAttribute.get("name") and attribute.get("value") != selectedAttribute.get("value"):
                            attribute["value"] = selectedAttribute.get("value")
            self._attributes = attributeDict
        return self._attributes

    def save(self):
        for formInput in self.request.POST:
            if formInput.startswith("attributes."):
                splitted = formInput.split(".")
                attribute = {splitted[1]: self.request.POST.get(formInput)}
                attributeIsBool = self.request.POST.get(formInput) in [True, False, "True", "False", "true", "false"]
                attributeModel = self.getExistingModelRecord(attributeName=splitted[1], attributeIsBool=attributeIsBool)
                if attributeModel:
                    attributeModel.attributeValue = self.request.POST.get(formInput) in [True, "True", "true"] or False
                    attributeModel.save()
                else:
                    self.saveNewRecord(attributeName=splitted[1], attributeValue=self.request.POST.get(formInput),
                                       attributeIsBool=attributeIsBool)


class ProfileAttributes(ActorAttributes):
    def __init__(self, *args, **kwargs):
        super(ProfileAttributes, self).__init__(*args, **kwargs)
        self.username = kwargs.get("username")

    @property
    def descriptionEnabled(self):
        self._descriptionEnabled = models.UserAccount.objects.get(username=self.username).actorDescriptionEnabled
        return self._descriptionEnabled

    @property
    def descriptionList(self):
        if self._descriptionList is None:
            self._descriptionList = sorted(chain(models.ActorDescriptionStringAttribute.objects.filter(username=self.username),
                                                 models.ActorDescriptionBooleanAttribute.objects.filter(username=self.username)))
        return self._descriptionList

    def getExistingModelRecord(self, attributeName, attributeIsBool):
        record = None
        database = None
        if attributeIsBool:
            database = models.ActorDescriptionBooleanAttribute
        else:
            database = models.ActorDescriptionStringAttribute

        try:
            record = database.objects.get(username=self.username, attributeName=attributeName)
        except database.DoesNotExist:
            pass
        return record

    def saveNewRecord(self, attributeName, attributeValue, attributeIsBool):
        if attributeIsBool:
            attributeModel = models.ActorDescriptionBooleanAttribute(username=self.username,
                                                                     attributeName = attributeName,
                                                                     attributeValue = attributeValue)
        else:
            attributeModel = models.ActorDescriptionStringAttribute(username=self.username,
                                                                    attributeName = attributeName,
                                                                    attributeValue = attributeValue)
        return attributeModel.save()


class CastingPostAttributes(ActorAttributes):
    def __init__(self, *args, **kwargs):
        super(CastingPostAttributes, self).__init__(*args, **kwargs)
        self.postID = kwargs.get("postID")

    @property
    def descriptionEnabled(self):
        self._descriptionEnabled = models.CastingPost.objects.get(postID=self.postID).descriptionEnabled
        return self._descriptionEnabled

    @property
    def descriptionList(self):
        if self._descriptionList is None:
            self._descriptionList = sorted(chain(models.ActorDescriptionStringAttribute.objects.filter(postID=self.postID),
                                                 models.ActorDescriptionBooleanAttribute.objects.filter(postID=self.postID)))
        return self._descriptionList

    def getExistingModelRecord(self, attributeName, attributeIsBool):
        record = None
        database = None
        if attributeIsBool:
            database = models.ActorDescriptionBooleanAttribute
        else:
            database = models.ActorDescriptionStringAttribute

        try:
            record = database.objects.get(postID=self.postID, attributeName=attributeName)
        except database.DoesNotExist:
            pass
        return record

    def saveNewRecord(self, attributeName, attributeValue, attributeIsBool):
        if attributeIsBool:
            attributeModel = models.ActorDescriptionBooleanAttribute(postID=self.postID,
                                                                     attributeName = attributeName,
                                                                     attributeValue = attributeValue)
        else:
            attributeModel = models.ActorDescriptionStringAttribute(postID=self.postID,
                                                                    attributeName = attributeName,
                                                                    attributeValue = attributeValue)
        return attributeModel.save()

