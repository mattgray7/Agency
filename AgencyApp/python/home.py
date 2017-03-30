from django.shortcuts import render

import helpers
import constants

def display(request, context):
    if request.POST:
        source = request.POST.get("source")
    else:
        source = helpers.getMessageFromKey(request, "source")
    # source is what got you to this page, possible sources are the possible sources that are supported
    context["source"] = source
    context["possibleSources"] = {"login": constants.LOGIN,
                                  "home": constants.HOME
                                  }
    context["possibleDestinations"] = {"post": constants.CREATE_POST,
                                       "event": constants.CREATE_EVENT,
                                       "home": constants.HOME
                                       }
    return render(request, 'AgencyApp/home.html', context=context)
