import post
import constants
import models


class WorkPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.WORK_POST
        super(WorkPostInstance, self).__init__(*args, **kwargs)
        self._database = models.WorkPost

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
            self.record.profession = self.request.POST.get("profession")
            self.record.paid = self.request.POST.get("paid", False) and True
            self.record.save()
            return True
        return False


class CreateWorkPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.WORK_POST
        super(CreateWorkPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            self._post = WorkPostInstance(request=self.request, postID=self.postID)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateWorkPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["profession"] = self.post.record.profession
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
