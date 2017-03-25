from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from models import User, Posting


def home(request):
    return render(request, 'AgencyApp/home.html', context={"welcomeMsg": "Welcome to The "
                                                                         "Agency"})

def profile(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
        context = {"user": user}
    except:
        context = {"username": username}
    return render(request, 'AgencyApp/profile.html', context)

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})