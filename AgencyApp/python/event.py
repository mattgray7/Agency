from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import AgencyApp.python as constants
import helpers

def create(request):
	source = helpers.getMessageFromKey(request, "source")
	context = {"possibleSources": {"login": constants.LOGIN_SUCCESS},
			   "source": source}
	return render(request, 'AgencyApp/event/create.html', {})