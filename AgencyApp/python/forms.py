from django import forms
from models import *
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
    loginSuccessDestination = forms.CharField(widget=forms.HiddenInput, required=False)

class CreateAccountForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput)
    firstName = forms.CharField(label="First Name", max_length=50)
    lastName = forms.CharField(label="Last Name", max_length=50)
    source = forms.CharField(widget=forms.HiddenInput, required=False)
    createSource = forms.CharField(widget=forms.HiddenInput, required=False)

class EditInterestsForm(forms.Form):
    work = forms.BooleanField(label="Work", required=False)
    crew = forms.BooleanField(label="Crew", required=False)
    collaboration = forms.BooleanField(label="Collaboration", required=False)
    source = forms.CharField(widget=forms.HiddenInput, required=False)
    editSource = forms.CharField(widget=forms.HiddenInput, required=False)

class EditPictureForm(forms.Form):
	profilePicture = forms.FileField(label="Profile Picture", required=False)
	editDestination = forms.CharField(widget=forms.HiddenInput, required=False)
	source = forms.CharField(widget=forms.HiddenInput, required=False)
	editSource = forms.CharField(widget=forms.HiddenInput, required=False)

class EditBackgroundForm(forms.Form):
	reel = forms.CharField(label="Reel Link", required=False, max_length=500)
	imdb = forms.CharField(label="IMDB Link", required=False, max_length=500)
	bio = forms.CharField(label="Bio", required=False, max_length=1000)
	editDestination = forms.CharField(widget=forms.HiddenInput, required=False)
	source = forms.CharField(widget=forms.HiddenInput, required=False)
	editSource = forms.CharField(widget=forms.HiddenInput, required=False)
