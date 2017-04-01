from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

import constants

def display(request, username, context):
    context["userAccount"] = None
    context["accountFound"] = False
    context["username"] = username
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        pass
    else:
        context["userAccount"] = UserAccount.objects.get(username=username)
        context["accountFound"] = True
    context["possibleSources"] = {"profile": constants.PROFILE}
    return render(request, "AgencyApp/profile.html", context)