from django.shortcuts import render
from forms import *

from django.contrib import messages

import datetime

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
        self._profileUserFilmography = None
        self._profileAdminProjects = None
        self._profileAvailability = None

    @property
    def profileLinks(self):
        if self._profileLinks is None:
            self._profileLinks = [{"url": self.profileUserAccount.imdbLink, "label": "IMDB"}]
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
                self._profileProfessions = self.profileUserAccount.profileProfessions
        return self._profileProfessions

    @property
    def profilePosts(self):
        if self._profilePosts is None:
            if self.profileUserAccount:
                self._profilePosts = {}
                self._profilePosts["events"] = models.EventPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["collaboration"] = models.CollaborationPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["work"] = models.WorkPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["projects"] = self.profileUserFilmography
                self._profilePosts["casting"] = models.CastingPost.objects.filter(poster=self.profileUserAccount.username)
        return self._profilePosts

    @property
    def profileUserFilmography(self):
        if not self._profileUserFilmography:
            self._profileUserFilmography = self.profileUserAccount.projects
        return self._profileUserFilmography

    @property
    def profileAdminProjects(self):
        if not self._profileAdminProjects:
            self._profileAdminProjects = {"hiring": [], "casting": []}
            adminProjects = [x.projectID for x in models.ProjectAdmin.objects.filter(username=self.profileUserAccount.username)]
            #adminPosts = [x.postID for x in models.PostAdmin.objects.filter(username=self.profileUserAccount)]
            if adminProjects:
                for projectID in adminProjects:
                    try:
                        projectPost = models.ProjectPost.objects.get(projectID=projectID)
                    except models.ProjectPost.DoesNotExist:
                        pass
                    else:
                        if projectPost.openJobs:
                            self._profileAdminProjects["hiring"].append(projectPost)
                        if projectPost.openRoles:
                            self._profileAdminProjects["casting"].append(projectPost)
        return self._profileAdminProjects

    @property
    def profileAvailability(self):
        if self._profileAvailability is None:
            if self.profileUserAccount and self.profileUserAccount.availability:
                self._profileAvailability = {"object": self.profileUserAccount.availability,
                                             "dates": []}
                if self.profileUserAccount.availabilityType == "openAvailability":
                    pass
                elif self.profileUserAccount.availabilityType == "daysOfWeek":
                    weekdays = models.AvailableWeekday.objects.filter(username=self.profileUserAccount.username)
                    if weekdays:
                        repeatWeeks = weekdays[0].repeatWeeks
                        for weekday in weekdays:
                            currentDate = datetime.date.today() + datetime.timedelta(days = 6 - weekdayNumber)
                            weekdayNumber = constants.WEEKDAYS.index(weekday.weekday)
                            self._profileAvailability["dates"].append(models.convertPythonDateStringToJS(currentDate))
                            for week in range(1, repeatWeeks):
                                currentDate += datetime.timedelta(days = 7)
                                self._profileAvailability["dates"].append(models.convertPythonDateStringToJS(currentDate))                    
                    pass
                elif self.profileUserAccount.availabilityType == "specifyDates_available":
                    dates = models.AvailabilityDate.objects.filter(username=self.profileUserAccount.username)
                    if dates:
                        for date in dates:
                            self._profileAvailability["dates"].append(models.convertPythonDateStringToJS(date.date))
                elif self.profileUserAccount.availabilityType == "specifyDates_unavailable":
                    pass
                else:
                    self._profileAvailability = None

                # Remove duplicates
                self._profileAvailability["dates"] = list(set(self._profileAvailability["dates"]))
        return self._profileAvailability

    @property
    def pageContext(self):
        self._pageContext = super(ProfileView, self).pageContext
        self._pageContext["displayName"] = self.displayName
        self._pageContext["viewingOwnProfile"] = self.userViewingOwnProfile

        self._pageContext["profileUserAccount"] = self.profileUserAccount
        self._pageContext["profileProfessions"] = self.profileProfessions
        self._pageContext["profileInterests"] = self.profileInterests
        self._pageContext["profilePosts"] = self.profilePosts
        self._pageContext["profileLinks"] = self.profileLinks
        self._pageContext["profileAdminProjects"] = self.profileAdminProjects
        self._pageContext["profileEndorsements"] = json.dumps(self.profileUserAccount.profileEndorsements)
        self._pageContext["profileAvailability"] = self.profileAvailability

        self._pageContext["filmography"] = json.dumps(self.profileUserFilmography)
        self._pageContext["actorDescriptionEnabled"] = self.profileUserAccount.actorDescriptionEnabled
        self._pageContext["icons"] = {"imdb": constants.IMDB_LOGO_PATH,
                                      "resume": constants.RESUME_ICON_PATH}

        self._pageContext["possibleDestinations"] = {"picture": constants.EDIT_PROFILE_PICTURE,
                                                     "media": constants.EDIT_PROFILE_PICTURE,
                                                     "background": constants.EDIT_BACKGROUND,
                                                     "interests": constants.EDIT_INTERESTS,
                                                     "filmography": constants.EDIT_FILMOGRAPHY,
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

