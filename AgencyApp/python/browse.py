from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict

# Create your views here.
from django.http import HttpResponseRedirect

import constants
import helpers
import genericViews as views
import models

import json


"""class BrowseChoiceView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(BrowseChoiceView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext["possibleSources"] = {"choice": constants.BROWSE_CHOICE}
        self._pageContext["possibleDestinations"] = {"events": constants.BROWSE_EVENTS,
                                                     "users": constants.BROWSE_USERS,
                                                     "posts": constants.BROWSE_POSTS,
                                                     "projects": constants.BROWSE_PROJECTS}
        return self._pageContext"""


class BrowseView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._nextPostID = None
        super(BrowseView, self).__init__(*args, **kwargs)
        self._followingPostIDs = None
        self._posterNameMap = None
        self._posterProfessionMap = None
 
    @property
    def nextPostID(self):
        if self._nextPostID is None:
            self._nextPostID = self.request.POST.get("postID") or helpers.getMessageFromKey(self.request, "postID")
        return self._nextPostID

    @property
    def followingPostIDs(self):
        """ List of IDs that the logged in user is following """
        if self._followingPostIDs is None:
            if self.request.user.username:
                self._followingPostIDs = [post.postID for post in models.PostFollow.objects.filter(username=self.request.user.username)]
        return self._followingPostIDs

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            if self.sourcePage in [constants.PROFILE, constants.VIEW_POST]:
                self._cancelSource = self.currentPage
            else:
                self._cancelSource = self.sourcePage
        return self._cancelSource

    @property
    def cancelButtonName(self):
        if self.sourcePage == constants.BROWSE:
            self._cancelButtonName = "Back to browse"
        elif self.sourcePage == constants.VIEW_POST:
            self._cancelButtonName = "Back to post"
        else:
            self._cancelButtonName = "Back"
        return self._cancelButtonName

    @property
    def cancelDestinationURL(self):
        if self._cancelDestinationURL is None:
            self._cancelDestinationURL = constants.URL_MAP.get(self.currentPage)
        return self._cancelDestinationURL

    @property
    def cancelButtonExtraInputs(self):
        if not self._cancelButtonExtraInputs:
            self._cancelButtonExtraInputs = {"postID": self.nextPostID}
        return json.dumps(self._cancelButtonExtraInputs)

    @property
    def cancelDestination(self):
        if self._cancelDestination is None:
            if self.sourcePage == constants.VIEW_POST:
                self._cancelDestination = self.sourcePage
            else:
                self._cancelDestination = constants.BROWSE
        return self._cancelDestination

    def cancelPage(self):
        pass

    @property
    def posterNameMap(self):
        if self._posterNameMap is None:
            self._posterNameMap = {}
            for account in models.UserAccount.objects.all():
                self._posterNameMap[account.username] = helpers.capitalizeName("{0} {1}".format(account.firstName, account.lastName))
        return self._posterNameMap

    @property
    def posterProfessionMap(self):
        if self._posterProfessionMap is None:
            self._posterProfessionMap = {}
            for name in self.posterNameMap:
                professions = models.Interest.objects.filter(username=name, mainInterest="work")
                if professions:
                    self._posterProfessionMap[name] = ", ".join([x.professionName for x in professions])
        return self._posterProfessionMap

    @property
    def pageContext(self):
        """self._pageContext["possibleViews"] = {"events": constants.BROWSE_EVENTS,
                                              "projects": constants.BROWSE_PROJECTS,
                                              "posts": constants.BROWSE_POSTS,
                                              "users": constants.BROWSE_USERS}"""
        self._pageContext["possibleDestinations"] = {"profile": constants.PROFILE,
                                                     "viewPost": constants.VIEW_POST,
                                                     "browse": constants.BROWSE}
        self._pageContext["followingPostIDs"] = self.followingPostIDs
        self._pageContext["posterNameMap"] = json.dumps(self.posterNameMap)
        self._pageContext["posterProfessionMap"] = json.dumps(self.posterProfessionMap)
        self._pageContext["browseType"] = self.currentPage
        self._pageContext["professionDict"] = json.dumps(constants.PROFESSIONS)
        return self._pageContext

"""
class BrowseEventsView(GenericBrowseView):
    def __init__(self, *args, **kwargs):
        super(BrowseEventsView, self).__init__(*args, **kwargs)
        self._eventList = None

    @property
    def eventList(self):
        if self._eventList is None:
            #TODO get 50 or so at a time
            self._eventList = models.EventPost.objects.all()
        return self._eventList

    @property
    def pageContext(self):
        self._pageContext = super(BrowseEventsView, self).pageContext
        self._pageContext["events"] = self.eventList
        return self._pageContext


class BrowseProjectsView(GenericBrowseView):
    def __init__(self, *args, **kwargs):
        super(BrowseProjectsView, self).__init__(*args, **kwargs)
        self._projectList = None

    @property
    def projectList(self):
        if self._projectList is None:
            #TODO get 50 or so at a time
            self._projectList = models.ProjectPost.objects.all()
        return self._projectList

    @property
    def pageContext(self):
        self._pageContext = super(BrowseProjectsView, self).pageContext
        self._pageContext["projects"] = self.projectList
        return self._pageContext


class BrowseUsersView(GenericBrowseView):
    def __init__(self, *args, **kwargs):
        super(BrowseUsersView, self).__init__(*args, **kwargs)
        self._userList = None
        self._actorUsers = None
        self._workerUsers = None
        self._otherUsers = None

    @property
    def actorUsers(self):
        if self._actorUsers is None:
            self._actorUsers = models.UserAccount.objects.filter(actingInterest=True)
        return self._actorUsers

    @property
    def workerUsers(self):
        if self._workerUsers is None:
            workerUsernames = [user.username for user in models.Interest.objects.filter(mainInterest="work")]
            self._workUsers = models.UserAccount.objects.filter(username__in=workerUsernames)
        return self._workUsers

    @property
    def otherUsers(self):
        if self._otherUsers is None:
            actorUsernames = [user.username for user in self.actorUsers]
            workerUsernames = [user.username for user in self.workerUsers]
            otherUsernames = set([user.username for user in models.UserAccount.objects.all()]) - set(actorUsernames) - set(workerUsernames)
            self._otherUsers = models.UserAccount.objects.filter(username__in=otherUsernames)
        return self._otherUsers

    @property
    def pageContext(self):
        self._pageContext = super(BrowseUsersView, self).pageContext
        self._pageContext["actors"] = self.actorUsers
        self._pageContext["workers"] = self.workerUsers
        self._pageContext["other"] = self.otherUsers
        return self._pageContext


class BrowsePostsView(GenericBrowseView):
    def __init__(self, *args, **kwargs):
        super(BrowsePostsView, self).__init__(*args, **kwargs)
        self._collabPostList = None
        self._workPostList = None
        self._castingPostList = None

    @property
    def collabPostList(self):
        if self._collabPostList is None:
            self._collabPostList = models.CollaborationPost.objects.all();
        return self._collabPostList

    @property
    def workPostList(self):
        if self._workPostList is None:
            self._workPostList = models.WorkPost.objects.all();
        return self._workPostList

    @property
    def castingPostList(self):
        if self._castingPostList is None:
            self._castingPostList = models.CastingPost.objects.all();
        return self._castingPostList

    @property
    def pageContext(self):
        self._pageContext = super(BrowsePostsView, self).pageContext
        self._pageContext["posts"] = {}
        self._pageContext["posts"]["collaboration"] = self.collabPostList
        self._pageContext["posts"]["work"] = self.workPostList
        self._pageContext["posts"]["casting"] = self.castingPostList
        return self._pageContext
"""

def _formatSearchPostResult(dbObject, extraFields):
    formattedResult = None
    if dbObject:
        formattedResult = {"title": dbObject.title,
                            "status": dbObject.status,
                            "postID": dbObject.postID,
                            "postPictureURL": dbObject.postPicture and dbObject.postPicture.url or constants.NO_PICTURE_PATH,
                            "poster": dbObject.poster,
                            "description": dbObject.description}
        if dbObject.projectID:
            try:
                proj = models.ProjectPost.objects.get(postID=dbObject.projectID)
            except models.ProjectPost.DoesNotExist:
                pass
            else:
                formattedResult["projectID"] = dbObject.projectID
                formattedResult["projectName"] = proj.title
        if extraFields:
            for fieldName in extraFields:
                fieldValue = dbObject.__dict__.get(fieldName) or ""
                formattedResult[fieldName] = fieldValue
    return formattedResult

def _appendPostResultsByType(existingList, filteredNewList, numResults, requiredFields):
    if existingList is not None and len(existingList) < numResults:
        if filteredNewList:
            for i, res in enumerate(filteredNewList):
                if(len(existingList) >= numResults):
                    break;

                # Check if post already matches, add if it doesn't
                existing = False
                for existingPost in existingList:
                    if existingPost["postID"] == res.postID:
                        existing = True
                        break
                if not existing:
                    existingList.append(_formatSearchPostResult(res, requiredFields))
    return existingList

def getJobsSearchResults(searchValue, numResults):
    results = []
    if searchValue and searchValue not in ["None", "null"]:
        # Search pattern is to look through professions, titles, project titles, and then descriptions
        requiredFields = ["compensationType", "compensationDescription", "startDate",
                          "endDate", "location", "profession", "hoursPerWeek"]

        # Look in profession
        results = _appendPostResultsByType(existingList=results,
                                           filteredNewList=models.WorkPost.objects.filter(profession__icontains=searchValue),
                                           numResults=numResults,
                                           requiredFields=requiredFields)

        # Look in name
        results = _appendPostResultsByType(existingList=results,
                                           filteredNewList=models.WorkPost.objects.filter(title__icontains=searchValue),
                                           numResults=numResults,
                                           requiredFields=requiredFields)

        # Look in description
        """results = _appendPostResultsByType(existingList=results,
                                           filteredNewList=models.WorkPost.objects.filter(description__icontains=searchValue),
                                           numResults=numResults,
                                           requiredFields=requiredFields)"""
    return results

def isBrowsePage(pageName):
    return pageName in [constants.BROWSE]