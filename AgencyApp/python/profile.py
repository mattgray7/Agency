from django.shortcuts import render
from forms import *

from django.contrib import messages

import constants
import models
import helpers
import genericViews as views
import post_project as projectPost


class ProfileView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._desiredProfileUsername = kwargs.get("username") or self.request.GET.get("username")
        super(ProfileView, self).__init__(*args, **kwargs)
        self._userViewingOwnProfile = False
        self._profileUserAccount = None
        self._profileProfessions = None
        self._profilePosts = None
        self._profileInterests = None
        self._profileLinks = None
        self._displayName = None

        self._profileProjects = None
        self._hasCurrentProjects = False
        self._hasPastProjects = False

        self._profileUserFilmography = None

    @property
    def profileLinks(self):
        if self._profileLinks is None:
            self._profileLinks = [{"url": self.profileUserAccount.imdbLink, "label": "IMDB"},
                                  {"url": self.profileUserAccount.reelLink, "label": "Reel"}]
        return self._profileLinks

    @property
    def displayName(self):
        if self._displayName is None:
            if self.profileUserAccount:
                self._displayName = helpers.capitalizeName("{0} {1}".format(self.profileUserAccount.firstName,
                                                                            self.profileUserAccount.lastName))
        return self._displayName

    @property
    def currentPageURL(self):
        if self._currentPageURL is None:
            self._currentPageURL = constants.URL_MAP.get(self.currentPage).format(self._desiredProfileUsername)
        return self._currentPageURL

    @property
    def userViewingOwnProfile(self):
        return self._desiredProfileUsername == self.username and self.request.user.is_authenticated()

    @property
    def profileUserAccount(self):
        if self._profileUserAccount is None:
            try:
                user = User.objects.get(username=self._desiredProfileUsername)
            except User.DoesNotExist:
                pass
            else:
                # get the rest of the profile attributes
                self._profileUserAccount = models.UserAccount.objects.get(username=self._desiredProfileUsername)
        return self._profileUserAccount

    @property
    def profileInterests(self):
        if self._profileInterests is None:
            self._profileInterests = {"work": None, "hire": None, "other": None}
            workInterests = models.Interest.objects.filter(username=self._desiredProfileUsername, mainInterest="work")
            hireInterests = models.Interest.objects.filter(username=self._desiredProfileUsername, mainInterest="hire")
            otherInterests = models.Interest.objects.filter(username=self._desiredProfileUsername, mainInterest="other")
            if workInterests:
                self._profileInterests["work"] = workInterests;
            if hireInterests:
                self._profileInterests["hire"] = hireInterests;
            if otherInterests:
                self._profileInterests["other"] = otherInterests;
        return self._profileInterests

    @property
    def profileProfessions(self):
        if self._profileProfessions is None:
            if self.profileUserAccount:
                try:
                    professions = models.Interest.objects.filter(username=self.profileUserAccount.username)
                except Interest.DoesNotExist:
                    pass
                else:
                    self._profileProfessions = [x.professionName for x in professions]
        return self._profileProfessions

    @property
    def profilePosts(self):
        if self._profilePosts is None:
            if self.profileUserAccount:
                self._profilePosts = {}
                self._profilePosts["events"] = models.EventPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["collaboration"] = models.CollaborationPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["work"] = models.WorkPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["projects"] = self.profileProjects
                self._profilePosts["casting"] = models.CastingPost.objects.filter(poster=self.profileUserAccount.username)
        return self._profilePosts

    @property
    def profileUserFilmography(self):
        if not self._profileUserFilmography:
            self._profileUserFilmography = self.profileUserAccount.projects
        return self._profileUserFilmography

    @property
    def profileProjects(self):
        if not self._profileProjects:
            self._profileProjects = []
            existingProjects = {}
            for role in models.CastingPost.objects.filter(actorName=self.profileUserAccount.username, status="Cast"):
                project = projectPost.getProjectObject(role.projectID)
                if project:
                    roleObj = {"postID": role.postID, "characterName": role.characterName}
                    if project.postID in existingProjects.keys():
                        existingProjectObjects[project.postID]["roles"].append(roleObj)
                    else:
                        existingProjects[project.postID] = {"project": project, "roles": [roleObj], "jobs": [],
                                                            "status": self._getProjectDisplayStatus(project), "creator": False}

            for job in models.WorkPost.objects.filter(workerName=self.profileUserAccount.username, status="Filled"):
                project = projectPost.getProjectObject(job.projectID)
                if project:
                    jobObj = {"postID": job.postID, "profession": job.profession}
                    if project.postID in existingProjects.keys():
                        existingProjects[project.postID]["jobs"].append(jobObj)
                    else:
                        existingProjects[project.postID] = {"project": project, "roles": [], "jobs": [jobObj],
                                                            "status": self._getProjectDisplayStatus(project), "creator": False}

            for project in models.ProjectPost.objects.filter(poster=self.profileUserAccount.username):
                if project.postID in existingProjects.keys():
                    existingProjects[project.postID]["creator"] = True
                else:
                    existingProjects[project.postID] = {"project": project, "roles": [], "jobs": [],
                                                       "status": self._getProjectDisplayStatus(project), "creator": True}
            for projectID in existingProjects.keys():
                existingProjects[projectID]["roles"] = json.dumps(existingProjects[projectID]["roles"])
                existingProjects[projectID]["jobs"] = json.dumps(existingProjects[projectID]["jobs"])
                if existingProjects[projectID]["status"] == "current":
                    self._hasCurrentProjects = True
                elif existingProjects[projectID]["status"] == "past":
                    self._hasPastProjects = True
                self._profileProjects.append(existingProjects[projectID])
        return self._profileProjects

    def _getProjectDisplayStatus(self, project):
        status = None
        if project.status in ["Pre-production", "In production", "Post production", "Screening"]:
            status = "current"
        elif project.status in ["Completed"]:
            status = "past"
        return status

    @property
    def pageContext(self):
        self._pageContext["displayName"] = self.displayName
        self._pageContext["viewingOwnProfile"] = self.userViewingOwnProfile
        self._pageContext["profileUserAccount"] = self.profileUserAccount
        self._pageContext["profileProfessions"] = self.profileProfessions
        self._pageContext["profileInterests"] = self.profileInterests
        self._pageContext["profilePosts"] = self.profilePosts
        self._pageContext["profileLinks"] = self.profileLinks
        self._pageContext["filmography"] = json.dumps(self.profileUserFilmography)

        self._pageContext["possibleDestinations"] = {"picture": constants.EDIT_PROFILE_PICTURE,
                                                     "background": constants.EDIT_BACKGROUND,
                                                     "interests": constants.EDIT_INTERESTS,
                                                     "viewPost": constants.VIEW_POST,
                                                     "actorDescription": constants.EDIT_ACTOR_DESCRIPTION
                                                     }
        return self._pageContext

    def process(self):
        if self.request.method == "POST":
            if self.formSubmitted:
                if self.form.is_valid():
                    messages.add_message(self.request, messages.INFO,
                                         "destination:{0}".format(constants.PROFILE))
                    return helpers.redirect(request=self.request,
                                            currentPage=self.currentPage,
                                            destinationPage=self.destinationPage)

        # Need to access pageContext before setting variables
        # !!!!!!!!!! Don't delete
        self.pageContext
        # !!!!!!!!!!
        if self._pageErrors:
            self._pageContext["errors"] = self.pageErrors
        return render(self.request, constants.HTML_MAP.get(self.currentPage), self.pageContext)

