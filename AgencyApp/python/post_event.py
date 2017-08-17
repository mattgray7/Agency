import post
import constants
import models


class EventPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.EVENT_POST
        self._projectID = kwargs.get("projectID")
        super(EventPostInstance, self).__init__(*args, **kwargs)
        self._database = models.EventPost

    def checkModelFormValues(self):
        return True

    def saveModelFormValues(self):
        if self.record:
            self.record.location = self.request.POST.get("location")
            self.record.date = self.request.POST.get("date")
            self.record.projectID = self.request.POST.get("projectID")
            self.record.admissionInfo = self.request.POST.get("admissionInfo")
            self.record.startTime = self.request.POST.get("startTime")
            self.record.endTime = self.request.POST.get("endTime")
            self.record.host = self.request.POST.get("host")
            self.record.save()
            return True
        return False


class CreateEventPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.EVENT_POST
        super(CreateEventPostView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext = super(CreateEventPostView, self).pageContext
        self._pageContext["hideStatus"] = True
        self._pageContext["defaultStatus"] = "Upcoming"
        self._pageContext["isEvent"] = True
        return self._pageContext

    def cancelPage(self):
        pass

    @property
    def post(self):
        if self._post is None:
            self._post = EventPostInstance(request=self.request, postID=self.postID, projectID=self.projectID,
                                           postType=constants.EVENT_POST, formSubmitted=self.formSubmitted)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateEventPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["location"] = self.post.record.location
            self._formInitialValues["date"] = self.post.record.date
            self._formInitialValues["startTime"] = self.post.record.startTime
            self._formInitialValues["endTime"] = self.post.record.endTime
            self._formInitialValues["host"] = self.post.record.host
            self._formInitialValues["admissionInfo"] = self.post.record.admissionInfo
            self._formInitialValues["projectID"] = self.projectID
        return self._formInitialValues


class ViewEventPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewEventPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = EventPostInstance(request=self.request, postID=self.postID, postType=constants.EVENT_POST)
        return self._post

