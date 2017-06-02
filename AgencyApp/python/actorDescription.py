import models
import constants
import post
import copy
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
            attributeDict = copy.deepcopy(constants.ACTOR_ATTRIBUTE_DICT)
            if self.selectedAttributes and len(self.selectedAttributes) > 0:
                for attribute in attributeDict:
                    for selectedAttribute in self.selectedAttributes:
                        if attribute.get("name") == selectedAttribute.get("name") and attribute.get("value") != selectedAttribute.get("value"):
                            attribute["value"] = selectedAttribute.get("value")
            self._attributes = attributeDict
        return self._attributes

    def save(self):
        if self.request.POST.get("descriptionEnabled") in ["false", "False", False, None]:
            self.deleteAndDisableDescriptionsInDB()
        else:
            self.enableDescriptionsInDB()
            for formInput in self.request.POST:
                if formInput.startswith("attributes."):
                    splitted = formInput.split(".")
                    attribute = {splitted[1]: self.request.POST.get(formInput)}
                    attributeIsBool = self.request.POST.get(formInput) in [True, False, "True", "False", "true", "false"]
                    attributeModel = self.getExistingModelRecord(attributeName=splitted[1], attributeIsBool=attributeIsBool)
                    if attributeModel:
                        if attributeIsBool:
                            attributeModel.attributeValue = self.request.POST.get(formInput) in [True, "True", "true"] or False
                        else:
                            attributeModel.attributeValue = self.request.POST.get(formInput)
                        attributeModel.save()
                    else:
                        self.saveNewRecord(attributeName=splitted[1], attributeValue=self.request.POST.get(formInput),
                                           attributeIsBool=attributeIsBool)

    def deleteDescriptions(self):
        return True

    def enabledDescriptionsInDB(self):
        return True


class ProfileAttributes(ActorAttributes):
    def __init__(self, *args, **kwargs):
        super(ProfileAttributes, self).__init__(*args, **kwargs)
        self.username = kwargs.get("username")
        self._userAccount = None

    @property
    def userAccount(self):
        if self._userAccount is None:
            try:
                self._userAccount = models.UserAccount.objects.get(username=self.username)
            except models.UserAccount.DoesNotExist:
                pass
        return self._userAccount

    @property
    def descriptionEnabled(self):
        self._descriptionEnabled = self.userAccount and self.userAccount.actorDescriptionEnabled or False
        return self._descriptionEnabled

    @property
    def descriptionList(self):
        if self._descriptionList is None:
            self._descriptionList = sorted(chain(models.ActorDescriptionStringAttribute.objects.filter(username=self.username),
                                                 models.ActorDescriptionBooleanAttribute.objects.filter(username=self.username)))
        return self._descriptionList

    def deleteAndDisableDescriptionsInDB(self):
        self.userAccount.actorDescriptionEnabled = False
        self.userAccount.save()
        models.ActorDescriptionStringAttribute.objects.filter(username=self.username).delete()
        models.ActorDescriptionBooleanAttribute.objects.filter(username=self.username).delete()
        return True

    def enableDescriptionsInDB(self):
        self.userAccount.actorDescriptionEnabled = True
        self.userAccount.save()

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
        self._castingPost = None

    @property
    def castingPost(self):
        if self._castingPost is None:
            self._castingPost = models.CastingPost.objects.get(postID=self.postID)
        return self._castingPost

    @property
    def descriptionEnabled(self):
        self._descriptionEnabled = self._castingPost.descriptionEnabled
        return self._descriptionEnabled

    @property
    def descriptionList(self):
        if self._descriptionList is None:
            self._descriptionList = sorted(chain(models.ActorDescriptionStringAttribute.objects.filter(postID=self.postID),
                                                 models.ActorDescriptionBooleanAttribute.objects.filter(postID=self.postID)))
        return self._descriptionList

    def deleteAndDisableDescriptionsInDB(self):
        self.castingPost.descriptionEnabled = False
        self.castingPost.save()
        models.ActorDescriptionStringAttribute.objects.filter(postID=self.postID).delete()
        models.ActorDescriptionBooleanAttribute.objects.filter(postID=self.postID).delete()
        return True

    def enableDescriptionsInDB(self):
        self.castingPost.descriptionEnabled = True
        self.castingPost.save()

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

