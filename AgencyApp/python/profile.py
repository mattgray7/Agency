from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount, Professions

import constants

def display(request, username, context):
    context["userAccount"] = None
    context["accountFound"] = False
    context["professionsFound"] = False
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
        	professions = Professions.objects.get(username=username)
        except User.DoesNotExist:
        	pass
        else:
        	context["professionsFound"] = True
        	context["userProfessions"] = professions
 
    context["possibleSources"] = {"profile": constants.PROFILE}
    return render(request, "AgencyApp/profile.html", context)