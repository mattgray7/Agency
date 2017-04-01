from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import helpers
import constants

def postType(request, context):
    context["possibleSources"] = {"login": constants.LOGIN,
                                  "home": constants.HOME,
                                  "createAccountFinish": constants.CREATE_BASIC_ACCOUNT_FINISH
                                  }
    return render(request, 'AgencyApp/choose/postType.html', context)