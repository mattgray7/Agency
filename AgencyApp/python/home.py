from django.shortcuts import render

import helpers
import constants

def display(request, context):
    """context["possibleSources"] = {"login": constants.LOGIN,
                                  "home": constants.HOME
                                  }"""
    context["source"] = constants.HOME
    context["possibleDestinations"] = {"post": constants.CREATE_POST,
                                       "event": constants.CREATE_EVENT,
                                       "home": constants.HOME,
                                       "createAccount": constants.CREATE_BASIC_ACCOUNT,
                                       "login": constants.LOGIN
                                       }
    context["default"] = constants.DEFAULT
    return render(request, 'AgencyApp/home.html', context=context)
