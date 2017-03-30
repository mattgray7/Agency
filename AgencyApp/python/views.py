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

baseContext = helpers.getBaseContext()

def displayHome(request):
    return home.display(request, baseContext)

def login(request):
    return account.loginUser(request, baseContext)

def logout(request):
    return account.logoutUser(request, baseContext)

def create_account(request):
    return account.createAccount(request, baseContext)

def create_selectInterests(request):
    return account.selectInterests(request, baseContext)

def create_selectProfessions(request):
    return account.selectProfessions(request, baseContext)

def create_addBackground(request):
    return account.addBackground(request, baseContext)

def create_accountFinish(request):
    return account.finish(request, baseContext)

def create_event(request):
    return event.create(request, baseContext)

def choose_postType(request):
    return choose.postType(request, baseContext)

def browse(request):
    return render(request, "AgencyApp/browse.html", baseContext)

def profile(request, username):
    context = baseContext
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