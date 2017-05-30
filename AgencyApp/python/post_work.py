import post
import constants
import models

import json

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
            self.record.profession = self.request.POST.get("professionSelect")
            self.record.paid = self.request.POST.get("paid", False) and True
            self.record.projectID = self.request.POST.get("projectID")
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
            self._post = WorkPostInstance(request=self.request, postID=self.postID, projectID=self.projectID, postType=constants.WORK_POST)
        return self._post

    @property
    def pageContext(self):
        self._pageContext = super(CreateWorkPostView, self).pageContext
        self._pageContext["professionList"] = json.dumps(constants.PROFESSIONS)
        self._pageContext["chosenProfession"] = self.post.record.profession
        self._pageContext["statusOptions"] = constants.WORK_STATUS_LIST

        return self._pageContext

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateWorkPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["profession"] = self.post.record.profession
            self._formInitialValues["paid"] = self.post.record.paid
            self._formInitialValues["status"] = self.post.record.status
            self._formInitialValues["projectID"] = self.projectID
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

