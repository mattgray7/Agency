from django.shortcuts import render
from forms import *

from helpers import getMessageFromKey
from django.contrib import messages


import constants
import models
import helpers
import genericViews as views


class ProfileView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._desiredProfileUsername = kwargs.get("username") or self.request.GET.get("username")
        super(ProfileView, self).__init__(*args, **kwargs)
        self._userViewingOwnProfile = False
        self._profileUserAccount = None
        self._profileProfessions = None
        self._profilePosts = None

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
    def profileProfessions(self):
        if self._profileProfessions is None:
            if self.profileUserAccount:
                try:
                    professions = models.Profession.objects.filter(username=self.profileUserAccount.username)
                except Profession.DoesNotExist:
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
                self._profilePosts["projects"] = models.ProjectPost.objects.filter(poster=self.profileUserAccount.username)
                self._profilePosts["casting"] = models.CastingPost.objects.filter(poster=self.profileUserAccount.username)
        return self._profilePosts

    @property
    def pageContext(self):
        self._pageContext["viewingOwnProfile"] = self.userViewingOwnProfile
        self._pageContext["profileUserAccount"] = self.profileUserAccount
        self._pageContext["profileProfessions"] = self.profileProfessions
        self._pageContext["profilePosts"] = self.profilePosts
        self._pageContext["possibleDestinations"] = {"picture": constants.EDIT_PROFILE_PICTURE,
                                                     "background": constants.EDIT_BACKGROUND,
                                                     "professions": constants.EDIT_PROFESSIONS,
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

