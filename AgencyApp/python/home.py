from django.shortcuts import render
from django.contrib import messages


from django.http import HttpResponseRedirect
from forms import *

import helpers
import constants
import helpers
import genericViews as views
import models
import browse
import copy
import datetime


class HomeView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(HomeView, self).__init__(*args, **kwargs)
        self._followedPosts = None

        self._featuredPosts = None
        self._featuredProjects = None
        self._featuredJobs = None
        self._featuredRoles = None
        self._featuredActors = None
        self._featuredProfessionals = None
        self._featuredEvents = None

        self._browseCategoryMap = {constants.WORK_POST: "jobs",
                                     constants.CASTING_POST: "roles",
                                     constants.PROJECT_POST: "projects",
                                     constants.EVENT_POST: "events"
                                     }
        self._postDateFields = ["startDate", "endDate", "startTime", "endTime"]

    @property
    def pageContext(self):
        self._pageContext = super(HomeView, self).pageContext
        self._pageContext["possibleSources"] = {"post": constants.CREATE_POST_CHOICE,
                                                "project": constants.CREATE_PROJECT_POST,
                                                "event": constants.CREATE_EVENT_POST,
                                                "home": constants.HOME,
                                                "createAccount": constants.CREATE_BASIC_ACCOUNT
                                                }
        self._pageContext["possibleDestinations"] = {"createProjectPost": constants.CREATE_PROJECT_POST,
                                                     "createPost": constants.CREATE_POST_CHOICE,
                                                     "browse": constants.BROWSE,
                                                     "viewPost": constants.VIEW_POST
                                                     }
        self._pageContext["followedPosts"] = json.dumps(self.followedPosts)
        self._pageContext["featuredPosts"] = json.dumps(self.featuredPosts)
        if self.userAccount:
            self._pageContext["lastLogout"] = self.userAccount.lastLogout
        return self._pageContext

    @property
    def featuredPosts(self):
        if self._featuredPosts is None:
            self._featuredPosts = {"projects": self.featuredProjects,
                                   "jobs": self.featuredJobs,
                                   "roles": self.featuredRoles,
                                   "actors": self.featuredActors,
                                   "professionals": self.featuredProfessionals,
                                   "events": self.featuredEvents,
                                   }
        return self._featuredPosts

    @property
    def featuredActors(self):
        if self._featuredActors is None:
            self._featuredActors = []
            actors = [x.username for x in models.Interest.objects.filter(mainInterest="work", professionName="Actor")]
            if actors:
                self._featuredActors = self._featuredActors + self._getUserObjectList(actors)
        return self._featuredActors

    @property
    def featuredProfessionals(self):
        if self._featuredProfessionals is None:
            self._featuredProfessionals = []

            # First check if user is hiring and for what positions
            hiringProfessions = []
            if self.userAccount and self.userAccount.adminPosts:
                for adminPost in self.userAccount.adminPosts:
                    if adminPost.postType == constants.WORK_POST:
                        if adminPost.status in ["Open", "Opening soon"]:
                            if adminPost.profession not in hiringProfessions:
                                hiringProfessions.append(adminPost.profession)

            if hiringProfessions:
                for profession in hiringProfessions:
                    interestUsers = [x.username for x in models.Interest.objects.filter(mainInterest="work", professionName=profession)]
                    if interestUsers:
                        self._featuredProfessionals = self._featuredProfessionals + self._getUserObjectList(interestUsers)
            if not self._featuredProfessionals:
                # Get all people looking for work
                workInterestUsers = [x.username for x in models.Interest.objects.filter(mainInterest="work")]
                if workInterestUsers:
                    self._featuredProfessionals = self._featuredProfessionals + self._getUserObjectList(workInterestUsers)
        return self._featuredProfessionals

    def _getUserObjectList(self, usernameList):
        userList = []
        userObjects = models.UserAccount.objects.filter(username__in=usernameList).order_by("-createdAt")
        if userObjects:
            for userObj in userObjects:
                userList.append(self._formatUser(userObj))
        return userList

    @property
    def featuredRoles(self):
        if self._featuredRoles is None:
            self._featuredRoles = []
            roles = models.CastingPost.objects.filter(status__in=["Open", "Opening soon"]).order_by("-createdAt")
            if roles:
                for role in roles:
                    self._featuredRoles.append(self._formatPost(role))
        return self._featuredRoles

    @property
    def featuredEvents(self):
        if self._featuredEvents is None:
            self._featuredEvents = []
            events = models.EventPost.objects.filter(startDate__gte=datetime.datetime.now())
            if events:
                for event in events:
                    self._featuredEvents.append(self._formatPost(event))
        return self._featuredEvents

    @property
    def featuredJobs(self):
        if self._featuredJobs is None:
            self._featuredJobs = []
            if self.userAccount and self.userAccount.workInterest:
                # Get interested professions
                interests = Interest.objects.filter(username=self.userAccount.username, mainInterest="work")
                if interests:
                    for interest in interests:
                        jobs = models.WorkPost.objects.filter(status__in=["Open", "Opening soon"],
                                                              profession=interest.professionName).order_by("-createdAt")
                        if jobs:
                            for job in jobs:
                                self._featuredJobs.append(self._formatPost(job))
                        else:
                            relatedProfessions = []
                            for field, professionList in constants.PROFESSIONS.iteritems():
                                if interest.professionName in professionList:
                                    relatedProfessions = professionList
                            if relatedProfessions:
                                jobs = models.WorkPost.objects.filter(status__in=["Open", "Opening soon"],
                                                                      profession__in=relatedProfessions).order_by("createdAt")
                                if jobs:
                                    for job in jobs:
                                        self._featuredJobs.append(self._formatPost(job))
        return self._featuredJobs

    @property
    def featuredProjects(self):
        if self._featuredProjects is None:
            self._featuredProjects = []
            if self.userAccount:
                # First get recently created projects
                projects = models.ProjectPost.objects.filter(createdAt__gte=self.userAccount.lastLogout)
                if not projects:
                    currentStatuses = copy.copy(constants.PROJECT_STATUS_LIST)
                    currentStatuses.remove("Completed")
                    projects = models.ProjectPost.objects.filter(status__in=currentStatuses)

                if projects:
                    for project in projects:
                        self._featuredProjects.append(self._formatPost(project))
        return self._featuredProjects

    @property
    def followedPosts(self):
        if self._followedPosts is None:
            self._followedPosts = []
            if self.userAccount and self.userAccount.followedPosts:
                for followedPost in self.userAccount.followedPosts:
                    self._followedPosts.append(self._formatPost(followedPost))
        return self._followedPosts

    def _formatUser(self, user):
        userDict = browse._formatSearchPostResult(user, [], "username")
        return userDict

    def _formatPost(self, postObj):
        postDict = browse._formatSearchPostResult(postObj,
                                                  browse.requiredFields[self._browseCategoryMap[postObj.postType]],
                                                  "postID")
        postDict["category"] = self._browseCategoryMap[postObj.postType];
        for fieldName in self._postDateFields:
            if postDict.get(fieldName):
                postDict[fieldName] = str(postDict[fieldName])
        return postDict

    def loginRequired(self):
        return not self.request.user.is_authenticated() and self.destinationPage in [constants.CREATE_EVENT_POST,
                                                                                     constants.CREATE_PROJECT_POST,
                                                                                     constants.CREATE_POST_CHOICE]

    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                if self.form.is_valid():
                    if self.loginRequired():
                        messages.add_message(self.request, messages.INFO,
                                             "destination:{0}".format(self.destinationPage))
                        self._destinationPage = constants.LOGIN
                    return helpers.redirect(request=self.request,
                                            currentPage=constants.HOME,
                                            destinationPage=self.destinationPage)

        # Need to access pageContext before setting variables
        # !!!!!!!!!! Don't delete
        self.pageContext
        # !!!!!!!!!!
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        return render(self.request, constants.HTML_MAP.get(constants.HOME), self.pageContext)

