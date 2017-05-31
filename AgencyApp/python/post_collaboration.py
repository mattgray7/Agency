import post
import constants
import models


class CollaborationPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.COLLABORATION_POST
        super(CollaborationPostInstance, self).__init__(*args, **kwargs)
        self._database = models.CollaborationPost

    def checkModelFormValues(self):
        valid = False
        if self.request.method == "POST":
            if len(self.request.POST.get("profession", "")) < 1:
                self.errors.append("Missing profession")
            else:
                valid = True
        return valid

    def saveModelFormValues(self):
        if self.record:
            self.record.profession = self.request.POST.get("profession", "")
            self.record.save()
            return True
        return False


class CreateCollaborationPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.COLLABORATION_POST
        super(CreateCollaborationPostView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
    	self._pageContext = super(CreateCollaborationPostView, self).pageContext
    	self._pageContext["hideStatus"] = True
    	return self._pageContext

    @property
    def post(self):
        if self._post is None:
            self._post = CollaborationPostInstance(request=self.request, postID=self.postID)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateCollaborationPostView, self).formInitialValues
        self._formInitialValues["postID"] = self.postID
        if self.post.record:
            self._formInitialValues["profession"] = self.post.record.profession
        return self._formInitialValues


class ViewCollaborationPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewCollaborationPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = CollaborationPostInstance(request=self.request, postID=self.postID)
        return self._post

