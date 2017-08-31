import post
import constants
import models
import helpers
import forms


class ProjectPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.PROJECT_POST
        super(ProjectPostInstance, self).__init__(*args, **kwargs)
        self._database = models.ProjectPost
        self._roles = None
        self._jobs = None
        self._events = None

    def checkModelFormValues(self):
        """TODO, only thing so far is status, which is optional, so return True"""
        return True

    def saveModelFormValues(self):
        newAdmin = models.ProjectAdmin(username=self.request.user.username,
                                       projectID=self.request.POST.get("projectID"))
        newAdmin.save()

        if self.record:
            self.record.location = self.request.POST.get("location")
            self.record.length = self.request.POST.get("length")
            self.record.union = self.request.POST.get("union", False) and True
            self.record.projectType = self.request.POST.get("projectType")
            self.record.projectID = self.projectID
            self.record.save()
        return True

    @property
    def roles(self):
        if not self._roles:
            projectRoles = models.CastingPost.objects.filter(projectID=self.postID)
            if projectRoles:
                self._roles = []
                for role in projectRoles:
                    newRole = {"post": role}
                    if role.status == "Cast":
                        try:
                            user = models.UserAccount.objects.get(username=role.actorName)
                        except models.UserAccount.DoesNotExist:
                            user = None
                        newRole["actor"] = user
                    self._roles.append(newRole)
        return self._roles

    @property
    def jobs(self):
        if not self._jobs:
            projectJobs = models.WorkPost.objects.filter(projectID=self.postID)
            if projectJobs:
                self._jobs = []
                for job in projectJobs:
                    newJob = {"post": job}
                    if job.status == "Filled":
                        try:
                            user = models.UserAccount.objects.get(username=job.workerName)
                        except models.UserAccount.DoesNotExist:
                            user = None
                        newJob["user"] = user
                    self._jobs.append(newJob)
        return self._jobs

    @property
    def events(self):
        if not self._events:
            projectEvents = models.EventPost.objects.filter(projectID=self.postID)
            if projectEvents:
                self._events = []
                for event in projectEvents:
                    newEvent = {"post": event}          # Simple for now, but want to keep same structure and may add more thing in the future(attendees, etc)
                    self._events.append(newEvent)
        return self._events


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
            self._post = ProjectPostInstance(request=self.request, postID=self.postID, projectID=self.postID, postType=constants.PROJECT_POST,
                                             formSubmitted=self.formSubmitted)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateProjectPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["status"] = self.post.record.status
            self._formInitialValues["location"] = self.post.record.location
            self._formInitialValues["length"] = self.post.record.length
            self._formInitialValues["union"] = self.post.record.union
            self._formInitialValues["projectType"] = self.post.record.projectType
        return self._formInitialValues

    @property
    def pageContext(self):
        self._pageContext = super(CreateProjectPostView, self).pageContext
        self._pageContext["defaultStatus"] = "In production"
        self._pageContext["roles"] = self.post.roles
        self._pageContext["jobs"] = self.post.jobs
        self._pageContext["events"] = self.post.events
        self._pageContext["forms"] = {"role": forms.CreateCastingPostForm,
                                      "job": forms.CreateWorkPostForm,
                                      "event": forms.CreateEventPostForm,
                                      "project": self.form}
        self._pageContext["isProject"] = True
        return self._pageContext

class ViewProjectPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewProjectPostView, self).__init__(*args, **kwargs)
        self._roles = None
        self._jobs = None
        self._events = None

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = ProjectPostInstance(request=self.request, postID=self.postID, postType=constants.PROJECT_POST)
        return self._post

    @property
    def pageContext(self):
        self._pageContext = super(ViewProjectPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"editPost": constants.EDIT_POST,
                                                     "viewPost": constants.VIEW_POST,
                                                     "createCasting": constants.CREATE_CASTING_POST,
                                                     "createWork": constants.CREATE_WORK_POST,
                                                     "createEvent": constants.CREATE_EVENT_POST
                                                     }
        self._pageContext["project"] = self.post
        self._pageContext["projectID"] = self.post.record.postID
        self._pageContext["isProject"] = True
        self._pageContext["roles"] = self.post.roles
        self._pageContext["jobs"] = self.post.jobs
        self._pageContext["events"] = self.post.events
        return self._pageContext

    @property
    def postTitle(self):
        if self._postTitle is None:
            if self.post and self.post.record:
                self._postTitle = self.post.record.title
        return self._postTitle

    @property
    def postSubTitles(self):
        if not self._postSubTitles:
            if self.post and self.post.record:
                self._postSubTitles = [self.post.record.projectType]
        return self._postSubTitles

    @property
    def postFieldsBySection(self):
        if not self._postFieldsBySection:
            if self.post and self.post.record:
                self._postFieldsBySection = {"head": {"Details": [{'id': 'status', 'value': self.post.record.status, 'label': 'Status'},
                                                                  {'id': 'location', 'value': self.post.record.location, 'label': 'Location'}],
                                                      "Description": [{'id': 'description', 'value': self.post.record.description, 'label': None}]
                                                     }
                                            }
        return self._postFieldsBySection


def getProjectObject(projectID):
    try:
        project = models.ProjectPost.objects.get(postID=projectID)
    except models.ProjectPost.DoesNotExist:
        pass
    else:
        return project
