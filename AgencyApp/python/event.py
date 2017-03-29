from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
from django.http import HttpResponseRedirect

def create(request):
	return render(request, 'AgencyApp/event/create.html', {})