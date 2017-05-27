import post
import constants
import models
import helpers

import post_project as projectPost
import json

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
            return True
        return False


class CreateCastingPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.CASTING_POST
        self._projectID = None
        self._project = None
        super(CreateCastingPostView, self).__init__(*args, **kwargs)

    def cancelPage(self):
        super(CreateCastingPostView, self).cancelPage()
        if self.request.POST.get(constants.CANCEL) == "True":
            # Delete post that was just created
            if not self.post.record.title:
                self.post.database.objects.filter(postID=self.postID).delete()

    @property
    def cancelButtonExtraInputs(self):
        if not self._cancelButtonExtraInputs:
            self._cancelButtonExtraInputs = {}
        if not self.post.record.title:
            # Skip to project should be done since this cancels the casting post
            self._cancelButtonExtraInputs["skipToProject"] = True

        if not self._cancelButtonExtraInputs.get("projectID"):
            self._cancelButtonExtraInputs["projectID"] = self.projectID
        if not self._cancelButtonExtraInputs.get("postID"):
            self._cancelButtonExtraInputs["postID"] = self.postID
        return json.dumps(self._cancelButtonExtraInputs)

    @property
    def project(self):
        if self._project is None:
            if self.projectID:
                self._project = projectPost.ProjectPostInstance(request=self.request, postID=self.projectID, postType=constants.PROJECT_POST)
        return self._project

    @property
    def projectID(self):
        """The project associated with the role being cast"""
        if self._projectID is None:
            projectID = self.request.POST.get("projectID") or helpers.getMessageFromKey(self.request, "projectID")
            if not projectID:
                try:
                    castingPost = models.CastingPost.objects.get(postID=self.postID)
                except models.CastingPost.DoesNotExist:
                    pass
                else:
                    projectID = castingPost.projectID
            self._projectID = projectID
        return self._projectID

    @property
    def pageContext(self):
        self._pageContext = super(CreateCastingPostView, self).pageContext
        self._pageContext["isProject"] = False
        self._pageContext.get("possibleDestinations", {})["casting"] = constants.VIEW_POST
        self._pageContext["viewProject"] = constants.VIEW_POST
        self._pageContext["project"] = self.project
        self._pageContext["projectID"] = self.projectID
        return self._pageContext

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.request.POST.get("postID")
            if not self._postID:
                self._postID = helpers.createUniqueID(destDatabase=models.CastingPost,
                                                      idKey="postID")
        return self._postID

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
        return self._formInitialValues


class ViewCastingPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        self._projectID = None
        self._project = None
        super(ViewCastingPostView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext = super(ViewCastingPostView, self).pageContext
        self._pageContext["project"] = self.project
        self._pageContext["projectID"] = self.projectID
        self._pageContext.get("possibleDestinations", {})["createCasting"] = constants.CREATE_CASTING_POST
        return self._pageContext

    @property
    def projectID(self):
        if self._projectID is None:
            projectID = self.request.POST.get("projectID", helpers.getMessageFromKey(self.request, "projectID"))
            if not projectID or projectID in ["null", "none"]:
                try:
                    projectID = models.CastingPost.objects.get(postID=self.postID).projectID
                except models.CastingPost.DoesNotExist:
                    pass
            self._projectID = projectID
        return self._projectID

    @property
    def project(self):
        if self._project is None:
            if self.projectID:
                self._project = projectPost.ProjectPostInstance(request=self.request, postID=self.projectID, postType=constants.PROJECT_POST)
        return self._project

    @property
    def post(self):
        if self._post is None:
            self._post = CastingPostInstance(request=self.request, postID=self.postID, projectID=self.projectID, postType=constants.CASTING_POST)
        return self._post


