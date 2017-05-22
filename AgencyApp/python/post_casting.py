import post
import constants
import models


class CastingPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.CASTING_POST
        super(CastingPostInstance, self).__init__(*args, **kwargs)
        self._database = models.CastingPost

    def checkModelFormValues(self):
        return True

    def saveModelFormValues(self):
        if self.record:
            self.record.paid = self.request.POST.get("paid", False) and True  #get value will be 'true' instead of True
            self.record.save()
            return True
        return False


class CreateCastingPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.CASTING_POST
        super(CreateCastingPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            self._post = CastingPostInstance(request=self.request, postID=self.postID)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateCastingPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["paid"] = self.post.record.paid
        return self._formInitialValues



class ViewWorkPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewWorkPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = WorkPostInstance(request=self.request, postID=self.postID)
        return self._post


