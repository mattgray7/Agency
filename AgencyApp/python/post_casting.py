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
            self.record.shortCharacterDescription = self.request.POST.get("shortCharacterDescription")
            self.record.actorName = self.request.POST.get("actorName")
            self.record.characterName = self.request.POST.get("characterName")
            self.record.hairColor = self.request.POST.get("hairColor")
            self.record.eyeColor = self.request.POST.get("eyeColor")
            self.record.complexion = self.request.POST.get("complexion")
            self.record.ageRange = self.request.POST.get("ageRange")
            self.record.gender = self.request.POST.get("gender")
            self.record.height = self.request.POST.get("height")
            self.record.weight = self.request.POST.get("weight")
            self.record.build = self.request.POST.get("build")

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
        self._selectFields = None
        self._actor = None

    @property
    def actor(self):
        if self._actor is None:
            if self.post.record.status == "Cast":
                try:
                    self._actor = models.UserAccount.objects.get(username=self.post.record.actorName)
                except models.UserAccount.DoesNotExist:
                    pass
        return self._actor

    @property
    def selectFields(self):
        if self._selectFields is None:
            self._selectFields = {"names": [], "options": {}, "defaults": {}}
            for field in constants.ACTOR_ATTRIBUTE_DICT:
                if field.get("options"):
                    name = field.get("name")
                    if name:
                        self._selectFields["names"].append(name)
                        if field.get("options"):
                            self._selectFields["options"][name] = field.get("options")
                        if self.formInitialValues.get(name):
                            self._selectFields["defaults"][name] = self.formInitialValues.get(name)
                        elif field.get("value"):
                            self._selectFields["defaults"][name] = field["value"]
        return self._selectFields

    @property
    def pageContext(self):
        self._pageContext = super(CreateCastingPostView, self).pageContext
        self._pageContext["selectFields"] = self.selectFields
        self._pageContext["defaultStatus"] = "Open"
        return self._pageContext

    @property
    def post(self):
        if self._post is None:
            self._post = CastingPostInstance(request=self.request, postID=self.postID, projectID=self.projectID, postType=constants.CREATE_CASTING_POST, formSubmitted=self.formSubmitted)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateCastingPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["paid"] = self.post.record.paid
            self._formInitialValues["characterName"] = self.post.record.characterName
            self._formInitialValues["shortCharacterDescription"] = self.post.record.shortCharacterDescription
            if self.actor:
                self._formInitialValues["actorName"] = self.actor.username
            self._formInitialValues["postID"] = self.post.record.postID
            self._formInitialValues["projectID"] = self.post.projectID
            for field in constants.ACTOR_ATTRIBUTE_DICT:
                self._formInitialValues[field["name"]] = getattr(self.post.record, field['name'])
        return self._formInitialValues


class ViewCastingPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewCastingPostView, self).__init__(*args, **kwargs)
        self._attributeListObject = None
        self._actor = None
        self._displayStatus = None  #current or past

    @property
    def actor(self):
        if self._actor is None:
            if self.post.record.status == "Cast":
                try:
                    self._actor = models.UserAccount.objects.get(username=self.post.record.actorName)
                except models.UserAccount.DoesNotExist:
                    pass
        return self._actor

    @property
    def pageContext(self):
        self._pageContext = super(ViewCastingPostView, self).pageContext
        self._pageContext["actor"] = self.actor
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

    """def createProjectChild(self):
        try:
            newRole = models.CastingPost.objects.get(postID=self.postID, projectID=self.projectID)
        except models.CastingPost.DoesNotExist:
            newRole = models.CastingPost(postID=self.postID, projectID=self.projectID, status="Open")
            newRole.save()"""
