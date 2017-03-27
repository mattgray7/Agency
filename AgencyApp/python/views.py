from django.shortcuts import render
from django.contrib.auth.models import User

from models import UserAccount
import account

def home(request):
    return render(request, 'AgencyApp/home.html', context={"welcomeMsg": "Welcome to The "
                                                                         "Agency"})

def login(request):
    return account.loginUser(request)

def logout(request):
    return account.logoutUser(request)

def createAccount(request):
    return account.createUser(request)

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