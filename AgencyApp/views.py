from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .forms import LoginForm, CreateAccountForm



def home(request):
    return render(request, 'AgencyApp/home.html', context={"welcomeMsg": "Welcome to The "
                                                                         "Agency"})

def login(request):
    print "in login"
    if request.method == 'POST':
        # Form submitted
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('email'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                print "VALID USER"
                return HttpResponseRedirect('/')
            else:
                print "Invalid USER"

    # login page navigated to 
    form = LoginForm()
    return render(request, 'AgencyApp/login.html', {'form': form})

def createAccount(request):
    if request.method == 'POST':
        print "request is post"
        # Form submitted
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('password') != form.cleaned_data.get('passwordConfirm'):
                print "Invalid password: {0} != {1}".format(form.cleaned_data.get('password'),form.cleaned_data.get('passwordConfirm'))
            else:
                try:
                    user = User.objects.create_user(username=form.cleaned_data.get('email'),
                                                    email=form.cleaned_data.get('email'), 
                                                    password=form.cleaned_data.get('password'))
                except IntegrityError:
                    print "Username is in use"
                else:
                    user.save()
                    return HttpResponseRedirect('/')

    else:
        print "request is not post"
    form = CreateAccountForm()
    return render(request, 'AgencyApp/createAccount.html', {'form': form})

def getWelcomeMsg(request):
    return JsonResponse({"response": "finished welcome msg"})

def profile(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
        context = {"userAccount": user}
    except:
        context = {"userNoAccount": username}
    print "context is {0}".format(context)
    return render(request, 'AgencyApp/profile.html', context)

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})