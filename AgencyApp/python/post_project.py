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
    def post(self):
        if self._post is None:
            self._post = ProjectPostInstance(request=self.request, postID=self.postID)
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

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = ProjectPostInstance(request=self.request, postID=self.postID)
        return self._post

