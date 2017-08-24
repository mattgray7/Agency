import post
import constants
import models
import helpers


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
            self.record.startDate = self.request.POST.get("startDate")
            self.record.endDate = self.request.POST.get("endDate")
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
            self._formInitialValues["startDate"] = self.post.record.startDate
            self._formInitialValues["endDate"] = self.post.record.endDate
            self._formInitialValues["startTime"] = self.post.record.startTime.strftime("%H:%M")
            self._formInitialValues["endTime"] = self.post.record.endTime.strftime("%H:%M")
            self._formInitialValues["host"] = self.post.record.host
            self._formInitialValues["admissionInfo"] = self.post.record.admissionInfo
            self._formInitialValues["projectID"] = self.projectID
        return self._formInitialValues


class ViewEventPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewEventPostView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext = super(ViewEventPostView, self).pageContext
        self._pageContext["isEvent"] = True
        return self._pageContext

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = EventPostInstance(request=self.request, postID=self.postID, postType=constants.EVENT_POST)
        return self._post

    @property
    def postSubTitles(self):
        if not self._postSubTitles:
            if self.post and self.post.record:
                if self.post.record.host:
                    self._postSubTitles = ["Hosted by {0}".format(self.post.record.title)]
        return self._postSubTitles

    @property
    def postFieldsBySection(self):
        if not self._postFieldsBySection:
            if self.post and self.post.record:
                self._postFieldsBySection = {"head": {"Details": [{'id': 'status', 'value': self.post.record.status, 'label': 'Status'},
                                                                  {'id': 'dates', 'value': helpers.getDateString(self.post.record.startDate, self.post.record.endDate), 'label': None},
                                                                  {'id': 'location', 'value': self.post.record.location, 'label': 'Location'},
                                                                  ],
                                                      },
                                             "body": {"Description": [{'id': 'description', 'value': self.post.record.description, 'label': None}
                                                                  ]
                                                      }
                                             }
                
                # Add project to front of list if it is linked
                if self.project and self.project.record:
                    self._postFieldsBySection["head"]["Details"] = [{'id': 'project', 'value': self.project.record.title, 'label': 'Project',
                                                                     'onclick': 'redirectToPost("{0}");'.format(self.project.record.postID)}] + self._postFieldsBySection["head"]["Details"]
        return self._postFieldsBySection

