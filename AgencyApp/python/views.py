from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from models import UserAccount
from helpers import getMessageFromKey

import constants
import helpers
import account
import event
import choose

def home(request):
    if request.POST:
        source = request.POST.get("source")
    else:
        source = helpers.getMessageFromKey(request, "source")
    return render(request, 'AgencyApp/home.html', context={"source": source,
                                                           "possibleSources": {"post": constants.CREATE_POST,
                                                                               "event": constants.CREATE_EVENT,
                                                                               "home": constants.HOME,
                                                                               "toolbarLogin": constants.TOOLBAR_LOGIN,
                                                                               "toolbarHome": constants.TOOLBAR_HOME}})

def login(request):
    return account.loginUser(request)

def logout(request):
    return account.logoutUser(request)

def create_account(request):
    return account.createAccount(request)

def create_selectInterests(request):
    return account.selectInterests(request)

def create_selectProfessions(request):
    return account.selectProfessions(request)

def create_addBackground(request):
    return account.addBackground(request)

def create_accountFinish(request):
    return account.finish(request)

def create_event(request):
    return event.create(request)

def choose_postType(request):
    return choose.postType(request)

def browse(request):
    return render(request, "AgencyApp/browse.html", {})

def profile(request, username):
    context = {"userAccount": None, "accountFound": False, "username": username}
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        pass
    else:
        context["userAccount"] = UserAccount.objects.get(username=username)
        context["accountFound"] = True
    return render(request, "AgencyApp/profile.html", context)

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})