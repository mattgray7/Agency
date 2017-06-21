import post
import constants
import models
import helpers


class ProjectPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.PROJECT_POST
        super(ProjectPostInstance, self).__init__(*args, **kwargs)
        self._database = models.ProjectPost

    def checkModelFormValues(self):
        """TODO, only thing so far is status, which is optional, so return True"""
        return True

    def saveModelFormValues(self):
        return True


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
            self._post = ProjectPostInstance(request=self.request, postID=self.postID, postType=constants.PROJECT_POST)
        return self._post

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateProjectPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["status"] = self.post.record.status
        return self._formInitialValues

    @property
    def pageContext(self):
        self._pageContext = super(CreateProjectPostView, self).pageContext
        self._pageContext["statusOptions"] = constants.PROJECT_STATUS_LIST
        self._pageContext["defaultStatus"] = "In production"
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
    def roles(self):
        if not self._roles:
            projectRoles = models.ProjectRole.objects.filter(projectID=self.postID)
            if projectRoles:
                self._roles = []
                for role in projectRoles:
                    newRole = {"role": role}
                    if role.status == "Cast":
                        try:
                            actor = models.UserAccount.objects.get(username=role.username)
                        except models.UserAccount.DoesNotExist:
                            actor = None
                        newRole["actor"] = actor
                    elif role.status == "Open":
                        try:
                            post = models.CastingPost.objects.get(postID=role.postID)
                        except models.CastingPost.DoesNotExist:
                            post = None
                        newRole["post"] = post
                    self._roles.append(newRole)
        return self._roles

    @property
    def jobs(self):
        if not self._jobs:
            projectJobs = models.ProjectJob.objects.filter(projectID=self.postID)
            if projectJobs:
                self._jobs = []
                for job in projectJobs:
                    try:
                        post = models.WorkPost.objects.get(postID=job.postID)
                    except models.WorkPost.DoesNotExist:
                        post = None
                    newJob = {"job": job, "post": post}
                    if job.status == "Filled":
                        try:
                            user = models.UserAccount.objects.get(username=job.username)
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

    @property
    def pageContext(self):
        self._pageContext = super(ViewProjectPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"edit": constants.CREATE_PROJECT_POST,
                                                     "viewPost": constants.VIEW_POST,
                                                     "createCasting": constants.CREATE_CASTING_POST,
                                                     "createWork": constants.CREATE_WORK_POST,
                                                     "createEvent": constants.CREATE_EVENT_POST
                                                     }
        self._pageContext["project"] = self.post
        self._pageContext["projectID"] = self.post.record.postID
        self._pageContext["roles"] = self.roles
        self._pageContext["jobs"] = self.jobs
        self._pageContext["events"] = self.events
        return self._pageContext

