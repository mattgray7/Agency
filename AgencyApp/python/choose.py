from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

def postType(request):
	return render(request, 'AgencyApp/choose/postType.html', {})