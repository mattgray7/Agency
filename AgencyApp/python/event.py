from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import constants
import helpers

def create(request, context):
    context["possibleSources"] = {"login": constants.LOGIN,
                                  "home": constants.HOME,
                                  "createAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH
                                  }
    return render(request, 'AgencyApp/event/create.html', context)