from django.shortcuts import render
from forms import *

from models import UserAccount, Profession, Event
from helpers import getMessageFromKey
from django.contrib import messages


import constants
import helpers
import views


class ProfileView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        self._desiredProfileUsername = kwargs.get("username") or self.request.GET.get("username")
        super(ProfileView, self).__init__(*args, **kwargs)
        self._userViewingOwnProfile = False
        self._profileUserAccount = None
        self._profileProfessions = None
        self._profileEvents = None

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
                self._profileUserAccount = UserAccount.objects.get(username=self._desiredProfileUsername)
        return self._profileUserAccount

    @property
    def profileProfessions(self):
        if self._profileProfessions is None:
            if self.profileUserAccount:
                try:
                    professions = Profession.objects.filter(username=self.profileUserAccount.username)
                except Profession.DoesNotExist:
                    pass
                else:
                    self._profileProfessions = [x.professionName for x in professions]
        return self._profileProfessions

    @property
    def profileEvents(self):
        if self._profileEvents is None:
            if self.profileUserAccount:
                try:
                    self._profileEvents = Event.objects.filter(poster=self.profileUserAccount.username)
                except Event.DoesNotExist:
                    pass
        return self._profileEvents

    @property
    def pageContext(self):
        self._pageContext["viewingOwnProfile"] = self.userViewingOwnProfile
        self._pageContext["profileUserAccount"] = self.profileUserAccount
        self._pageContext["profileUsername"] = self._desiredProfileUsername
        self._pageContext["profileProfessions"] = self.profileProfessions
        self._pageContext["profileEvents"] = self.profileEvents
        self._pageContext["possibleDestinations"] = {"picture": constants.EDIT_PROFILE_PICTURE,
                                                     "background": constants.EDIT_BACKGROUND,
                                                     "professions": constants.EDIT_PROFESSIONS,
                                                     "interests": constants.EDIT_INTERESTS,
                                                     "viewEvent": constants.VIEW_EVENT
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

