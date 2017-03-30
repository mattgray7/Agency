from django.shortcuts import render

import helpers
import constants

def display(request, context):
    if request.POST:
        source = request.POST.get("source")
    else:
        source = helpers.getMessageFromKey(request, "source")
    context["source"] = source
    context["possibleSources"] = {"post": constants.CREATE_POST,
                                  "event": constants.CREATE_EVENT,
                                  "home": constants.HOME,
                                  "toolbarLogin": constants.TOOLBAR_LOGIN,
                                  "toolbarHome": constants.TOOLBAR_HOME
                                  }
    return render(request, 'AgencyApp/home.html', context=context)
