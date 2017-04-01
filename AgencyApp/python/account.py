from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponseRedirect
from forms import LoginForm, CreateAccountForm, SelectInterestsForm, SelectProfessionsForm, AddBackgroundForm
from models import UserAccount, Professions
from helpers import getMessageFromKey, capitalizeName

import constants
import helpers

def loginUser(request, context):
    errors = []
    if request.method == 'POST':
        # Form submitted
        form = LoginForm(request.POST)
        if form.is_valid():
            username = _getProfileNameFromEmail(form.cleaned_data.get('email'))
            if username is None:
                errors.append("{0} is not a registered email.".format(form.cleaned_data.get('email')))
            else:
                user = authenticate(username=username, password=form.cleaned_data.get('password'))
                if user is not None:
                    # Login was a success
                    login(request, user)
                    loginDestination = form.cleaned_data.get('loginSuccessDestination')

                    messages.add_message(request, messages.INFO, "source:{0}".format(constants.LOGIN))
                    if loginDestination == constants.CREATE_POST:
                        return HttpResponseRedirect('/create/post/choose')
                    elif loginDestination == constants.CREATE_EVENT:
                        return HttpResponseRedirect('/create/event/')
                    else:
                        return HttpResponseRedirect('/')
                else:
                    errors.append("Email and password do not match.")
        else:
            if request.POST.get("loginSuccessDestination"):
                loginSuccessDestination = request.POST.get("loginSuccessDestination")
                context["form"] = LoginForm(initial={'loginSuccessDestination': loginSuccessDestination})
                if loginSuccessDestination == constants.CREATE_POST:
                    errors.append("You must login to create a post.")
                elif loginSuccessDestination == constants.CREATE_EVENT:
                    errors.append("You must login to create an event.")
    
    if not context.get("form"):
        context["form"] = LoginForm()
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/login.html', context)


def logoutUser(request, context):
    logout(request)
    return HttpResponseRedirect('/')


def createAccount(request, context):
    errors = []
    if request.method == 'POST':
        # Form submitted
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            if _emailIsRegistered(form.cleaned_data.get('email')):
                errors.append("Email already in use.")
            else:
                if form.cleaned_data.get('password') != form.cleaned_data.get('passwordConfirm'):
                    errors.append("Passwords don't match.")
                else:
                    firstName = capitalizeName(form.cleaned_data.get('firstName'))
                    lastName = capitalizeName(form.cleaned_data.get('lastName'))
                    username = _getProfileNameFromName(firstName.lower(), lastName.lower())
                    
                    user = User.objects.create_user(username=username,
                                                    email=form.cleaned_data.get('email'), 
                                                    password=form.cleaned_data.get('password'),
                                                    first_name=firstName,
                                                    last_name=lastName)
                    userAccount = UserAccount(email=form.cleaned_data.get('email'),
                                              username=username,
                                              setupComplete=False)
                    saveSuccess = True
                    try:
                        user.save()
                    except:
                        saveSuccess = False
                        errors.append("Unable to save in User db.")
                    else:
                        try:
                            userAccount.save()
                        except:
                            saveSuccess = False
                            errors.append("Unable to save in UserAccount db.")
                            #TODO delete account from User db
                    if saveSuccess:
                        print "Successfully created account."
                        login(request, user)

                        messages.add_message(request, messages.INFO,
                                             "source:{0}".format(constants.CREATE_BASIC_ACCOUNT_FINISH))
                        return HttpResponseRedirect('/account/create/finish/')

    context["form"] = CreateAccountForm()
    if errors:
        print "Create account errors: {0}".format(errors)
        context["errors"] = errors
    return render(request, 'AgencyApp/account/create.html', context)


def finish(request, context):
    if request.POST:
        source = request.POST.get("source")
    else:
        source = helpers.getMessageFromKey(request, "source")
    context["source"] = source
    context["possibleSources"] = {"finish": constants.CREATE_BASIC_ACCOUNT_FINISH}
    return render(request, 'AgencyApp/account/finish.html', context)


def selectInterests(request, context):
    errors = []
    if request.method == "POST":
        form = SelectInterestsForm(request.POST)
        if form.is_valid():
            workSelected = form.cleaned_data.get('work', False)
            crewSelected = form.cleaned_data.get('crew', False)
            collabSelected = form.cleaned_data.get('collaboration', False)
            if not workSelected and not crewSelected and not collabSelected:
                errors.append("You must choose at least one option you are interested in.")
            else:
                username = getMessageFromKey(request, "username")
                userAccount = UserAccount.objects.get(username=username)
                userAccount.workInterest = workSelected
                userAccount.crewInterest = crewSelected
                userAccount.collaborationInterest = collabSelected
                try:
                    userAccount.save()
                except:
                    errors.append("Could not connect to UserAccount database")
                else:
                    print "User successfully saved with work:{0}, crew:{1}, collab:{2}".format(workSelected, crewSelected, collabSelected)

                user = User.objects.get(username=username)
                #TODO when to log user in
                #login(request, user)
                messages.add_message(request, messages.INFO, "username:{0}".format(username))

                if workSelected:
                    return HttpResponseRedirect('/create/professions')
                else:
                    return HttpResponseRedirect('/create/finish')

                return HttpResponseRedirect('/')
    context["form"] = SelectInterestsForm()
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/interests.html', context)

def selectProfessions(request, context):
    errors = []
    if request.method == "POST":
        form = SelectProfessionsForm(request.POST)
        if form.is_valid():
            actor = form.cleaned_data.get('actor', False)
            director = form.cleaned_data.get('director', False)
            writer = form.cleaned_data.get('writer', False)
            cinematographer = form.cleaned_data.get('cinematographer', False)
            other = form.cleaned_data.get('work', '')

            if actor == director == writer == cinematographer == False and other == "":
                errors.append("You must select what line of work you are looking for.")
            else:
                #username = getMessageFromKey(request, "username")
                username = request.user.username
                professions = Professions(username=username, actor=actor, director=director,
                                          cinematographer=cinematographer, other=other)
                #TODO check if user profession already exists?
                try:
                    professions.save()
                except:
                    errors.append("Could not connect to Profession db.")
                else:
                    return HttpResponseRedirect('/create/background')
    context["form"] = SelectProfessionsForm()
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/professions.html', context)


def addBackground(request, context):
    errors = []
    if request.method == "POST":
        form = AddBackgroundForm(request.POST)
        if form.is_valid():
            pic = form.cleaned_data.get('profilePicture')
            reel = form.cleaned_data.get('reel')
            imdb = form.cleaned_data.get('imdb')
            bio = form.cleaned_data.get('bio')

            #username = getMessageFromKey(request, "username")
            username = request.user.username

            userAccount = UserAccount.objects.get(username=username)
            userAccount.profilePicture = pic
            userAccount.reelLink = reel
            userAccount.imdbLink = imdb
            userAccount.bio = bio
            
            try:
                userAccount.save()
            except:
                errors.append("Could not connect to UserAccount db.")
            else:
                return HttpResponseRedirect('/create/finish')
    context["form"] = AddBackgroundForm()
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/background.html', context)

def _emailIsRegistered(email):
    existingUsers = User.objects.filter(email=email)
    return len(existingUsers) > 0


def _getProfileNameFromEmail(email):
    try:
        user = UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
        return None
    else:
        return user.username


def _getProfileNameFromName(firstName, lastName):
    tempName = "{0}{1}".format(firstName, lastName)
    numConflictingNames = len(UserAccount.objects.filter(username__startswith=tempName))
    if numConflictingNames > 0:
        # if mattgray exists, new name will be mattgray1
        tempName += str(numConflictingNames)
    return tempName



