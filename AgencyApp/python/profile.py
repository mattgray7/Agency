from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount, Profession, Event

import constants

def display(request, username, context):
    context["userAccount"] = None
    context["accountFound"] = False
    context["professionsFound"] = False
    context["eventsFound"] = False
    context["username"] = username
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass
    else:
        context["userAccount"] = UserAccount.objects.get(username=username)
        context["accountFound"] = True

        # get professions
        try:
        	professions = Profession.objects.filter(username=username)
        except Profession.DoesNotExist:
        	pass
        else:
        	# TODO still set to True even if user removes all professions
        	context["professionsFound"] = True
        	context["userProfessions"] = [x.professionName for x in professions]   	

        try:
            events = Event.objects.filter(poster=username)
        except Event.DoesNotExist:
            pass
        else:
            context["eventsFound"] = True
            context["events"] = events

    context["source"] = constants.PROFILE
    context["possibleDestinations"] = {"picture": constants.EDIT_PROFILE_PICTURE,
                                       "background": constants.EDIT_BACKGROUND,
                                       "professions": constants.EDIT_PROFESSIONS,
                                       "interests": constants.EDIT_INTERESTS}
    return render(request, "AgencyApp/profile.html", context)