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
import home

getBaseContext = helpers.getBaseContext

def displayHome(request):
    return home.display(request, getBaseContext())

def login(request):
    return account.loginUser(request, getBaseContext())

def logout(request):
    return account.logoutUser(request, getBaseContext())

def createAccount(request):
    return account.createAccount(request, getBaseContext())

def addPicture(request):
    return account.addPicture(request, getBaseContext())

def create_selectInterests(request):
    return account.selectInterests(request, getBaseContext())

def create_selectProfessions(request):
    return account.selectProfessions(request, getBaseContext())

def create_addBackground(request):
    return account.addBackground(request, getBaseContext())

def createAccountFinish(request):
    return account.finish(request, getBaseContext())

def createEvent(request):
    return event.create(request, getBaseContext())

def choosePostType(request):
    return choose.postType(request, getBaseContext())

def browse(request):
    return render(request, "AgencyApp/browse.html", getBaseContext())

def profile(request, username):
    context = getBaseContext()
    context["userAccount"] = None
    context["accountFound"] =False
    context["username"] = username
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