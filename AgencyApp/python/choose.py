from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import helpers
import constants

def postType(request, context):
	if request.POST:
		source = request.POST.get("source")
	else:
		source = helpers.getMessageFromKey(request, "source")
	context["source"]=  source
	context["possibleSources"] = {"login": constants.LOGIN_SUCCESS,
			   					  "home": constants.HOME
			   					  }
	return render(request, 'AgencyApp/choose/postType.html', context)