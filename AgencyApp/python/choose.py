from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

import helpers
import AgencyApp.python as constants

def postType(request):
	if request.POST:
		source = request.POST.get("source")
	else:
		source = helpers.getMessageFromKey(request, "source")
	print "source is {0}".format(source)
	context = {"source": source,
			   "possibleSources": {"login": constants.LOGIN_SUCCESS,
			   					   "home": constants.HOME}
			   }
	return render(request, 'AgencyApp/choose/postType.html', context)