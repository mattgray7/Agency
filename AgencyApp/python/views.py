from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

import constants
import helpers
import account
import event
import choose
import home
import profile

getBaseContext = helpers.getBaseContext

def displayHome(request):
    return home.display(request, getBaseContext(request))

def login(request):
    return account.loginUser(request, getBaseContext(request))

def logout(request):
    return account.logoutUser(request, getBaseContext(request))

def createAccount(request):
    return account.createAccount(request, getBaseContext(request))

def editInterests(request):
    return account.editInterests(request, getBaseContext(request))

def editPicture(request):
    return account.editPicture(request, getBaseContext(request))

def editProfessions(request):
    return account.editProfessions(request, getBaseContext(request))

def editBackground(request):
    return account.editBackground(request, getBaseContext(request))

def createAccountFinish(request):
    return account.finish(request, getBaseContext(request))

def createEvent(request):
    return event.create(request, getBaseContext(request))

def choosePostType(request):
    return choose.postType(request, getBaseContext(request))

def browse(request):
    return render(request, "AgencyApp/browse.html", getBaseContext(request))

def displayProfile(request, username):
    return profile.display(request, username, getBaseContext(request))

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})