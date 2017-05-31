import post
import constants
import models


class EventPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.EVENT_POST
        super(EventPostInstance, self).__init__(*args, **kwargs)
        self._database = models.EventPost

    def checkModelFormValues(self):
        valid = False
        if self.request.method == "POST":
            if len(self.request.POST.get("location")) < 1:
                self.errors.append("Missing location")
            else:
                valid = True
        return valid

    def saveModelFormValues(self):
        if self.record:
            self.record.location = self.request.POST.get("location", "")
            self.record.date = self.request.POST.get("date", "")
            self.record.projectID = self.request.POST.get("projectID")
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
        return self._pageContext

    @property
    def post(self):
        if self._post is None:
            self._post = EventPostInstance(request=self.request, postID=self.postID, projectID=self.projectID)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateEventPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["location"] = self.post.record.location
            self._formInitialValues["date"] = self.post.record.date
            self._formInitialValues["projectID"] = self.projectID
        return self._formInitialValues


class ViewEventPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewEventPostView, self).__init__(*args, **kwargs)

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = EventPostInstance(request=self.request, postID=self.postID)
        return self._post

