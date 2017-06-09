from django.shortcuts import render
from django.contrib import messages


from django.http import HttpResponseRedirect
from forms import *

import helpers
import constants
import helpers
import genericViews as views
import models


class HomeView(views.GenericFormView):
    def __init__(self, *args, **kwargs):
        super(HomeView, self).__init__(*args, **kwargs)

    @property
    def pageContext(self):
        self._pageContext["possibleSources"] = {"post": constants.CREATE_POST_CHOICE,
                                                "project": constants.CREATE_PROJECT_POST,
                                                "event": constants.CREATE_EVENT_POST,
                                                "home": constants.HOME,
                                                "createAccount": constants.CREATE_BASIC_ACCOUNT
                                                }
        return self._pageContext

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

