import post
import constants
import models
import helpers


class ProjectPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.PROJECT_POST
        super(ProjectPostInstance, self).__init__(*args, **kwargs)
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


class CreateProjectPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.PROJECT_POST
        super(CreateProjectPostView, self).__init__(*args, **kwargs)

    @property
    def projectID(self):
        if self._projectID is None:
            self._projectID = self.request.POST.get("projectID", helpers.getMessageFromKey(self.request, "projectID"))
            if not self._projectID:
                self._projectID = helpers.createUniqueID(destDatabase=models.ProjectPost,
                                                        idKey="postID")
        return self._projectID

    @property
    def postID(self):
        if self._postID is None:
            self._postID = self.projectID
        return self._postID

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.currentPage
        return self._cancelSource 

    @property
    def cancelButtonExtraInputs(self):
        if not self._cancelButtonExtraInputs:
            self._cancelButtonExtraInputs = super(CreateProjectPostView, self).cancelButtonExtraInputs or {}
        self._cancelButtonExtraInputs["projectID"] = self.postID
        return self._cancelButtonExtraInputs

    def cancelPage(self):
        pass

    @property
    def post(self):
        if self._post is None:
            self._post = ProjectPostInstance(request=self.request, postID=self.postID, postType=constants.PROJECT_POST)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateProjectPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["status"] = self.post.record.status
        return self._formInitialValues


class ViewProjectPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewProjectPostView, self).__init__(*args, **kwargs)
        self._castingPosts = None
        self._workPosts = None

    @property
    def castingPosts(self):
        if self._castingPosts is None:
            self._castingPosts = models.CastingPost.objects.filter(projectID=self.postID)
        return self._castingPosts

    @property
    def workPosts(self):
        if self._workPosts is None:
            self._workPosts = models.WorkPost.objects.filter(projectID=self.postID)
        return self._workPosts

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = ProjectPostInstance(request=self.request, postID=self.postID, postType=constants.PROJECT_POST)
        return self._post

    @property
    def pageContext(self):
        self._pageContext = super(ViewProjectPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"edit": constants.CREATE_PROJECT_POST,
                                                     "createCasting": constants.CREATE_CASTING_POST,
                                                     "viewCasting": constants.VIEW_POST,
                                                     "createWork": constants.CREATE_WORK_POST,
                                                     "viewWork": constants.VIEW_POST,
                                                     "viewPost": constants.VIEW_POST}
        self._pageContext["castingPosts"] = self.castingPosts
        self._pageContext["workPosts"] = self.workPosts
        self._pageContext["project"] = self.post
        self._pageContext["projectID"] = self.post.record.postID
        return self._pageContext

