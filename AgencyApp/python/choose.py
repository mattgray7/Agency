from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import helpers
import AgencyApp.python as constants

def postType(request):
	source = helpers.getMessageFromKey(request, "source")
	context = {"source": source,
			   "possibleSources": {"login": constants.LOGIN_SUCCESS}
			   }
	return render(request, 'AgencyApp/choose/postType.html', {})