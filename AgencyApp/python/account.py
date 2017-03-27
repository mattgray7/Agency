from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponseRedirect
from forms import LoginForm, CreateAccountForm
from models import UserAccount


def loginUser(request):
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
                    login(request, user)
                    messages.add_message(request, messages.INFO, "login_success")
                    return HttpResponseRedirect('/')
                else:
                    errors.append("Email and password do not match.")

    context = {"form": LoginForm()}
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/login.html', context)


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')


def createUser(request):
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
                    firstName = _capitalizeName(form.cleaned_data.get('firstName'))
                    lastName = _capitalizeName(form.cleaned_data.get('lastName'))
                    username = _getProfileNameFromName(firstName.lower(), lastName.lower())
                    
                    user = User.objects.create_user(username=username,
                                                    email=form.cleaned_data.get('email'), 
                                                    password=form.cleaned_data.get('password'),
                                                    first_name=firstName,
                                                    last_name=lastName)
                    userAccount = UserAccount(email=form.cleaned_data.get('email'),
                                                username=username)
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
                        print "Successfully logged in."

                        messages.add_message(request, messages.INFO, "create_success")
                        return HttpResponseRedirect('/')

    print "Create account errors: {0}".format(errors)

    context = {"form": CreateAccountForm()}
    if errors:
        context["errors"] = errors
    return render(request, 'AgencyApp/account/create.html', context)


def _capitalizeName(name):
    """Capitalizes first letter of names (eg matt->Matt, smith-pelly->Smith-Pelly, 
       deBrincat->DeBrincat)

    :param str name: The name to capitalize
    :return str: The capitalized name
    """
    finalName = ''
    first = True
    for char in name:
        if first:
            finalName += char.upper()
            first = False
        elif char in ['-', ' ']:
            finalName += char
            first=True
        else:
            finalName += char
    return finalName



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



