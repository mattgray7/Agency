import post
import constants
import models


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
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.currentPage
        return self._cancelSource 

    def cancelPage(self):
        pass

    @property
    def post(self):
        if self._post is None:
            self._post = ProjectPostInstance(request=self.request, postID=self.postID, postType=constants.PROJECT_POST)
            print self._post
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

    @property
    def castingPosts(self):
        if self._castingPosts is None:
            self._castingPosts = models.CastingPost.objects.filter(projectID=self.postID)
        return self._castingPosts

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
                                                     "viewCasting": constants.VIEW_POST}
        self._pageContext["castingPosts"] = self.castingPosts
        self._pageContext["project"] = self.post
        self._pageContext["projectID"] = self.post.record.postID
        return self._pageContext

