from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import constants
import helpers

def create(request):
	if request.POST:
		source = request.POST.get("source")
	else:
		source = helpers.getMessageFromKey(request, "source")
	context = {"source": source,
			   "possibleSources": {"login": constants.LOGIN_SUCCESS,
			   					   "home": constants.HOME}
			   }
	return render(request, 'AgencyApp/event/create.html', context)