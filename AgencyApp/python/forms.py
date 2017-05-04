from django import forms
from models import *
from django.contrib.auth.models import User


class BaseForm(forms.Form):
    source = forms.CharField(widget=forms.HiddenInput, required=False)
    next = forms.CharField(widget=forms.HiddenInput, required=False)
    destination = forms.CharField(widget=forms.HiddenInput, required=False)

class LoginForm(BaseForm):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)

class CreateAccountForm(BaseForm):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput)
    firstName = forms.CharField(label="First Name", max_length=50)
    lastName = forms.CharField(label="Last Name", max_length=50)

class EditInterestsForm(BaseForm):
    work = forms.BooleanField(label="Work", required=False)
    crew = forms.BooleanField(label="Crew", required=False)
    collaboration = forms.BooleanField(label="Collaboration", required=False)

class EditPictureForm(BaseForm):
    profilePicture = forms.FileField(label="New profile picture", required=False)

class EditBackgroundForm(BaseForm):
    reel = forms.CharField(label="Reel Link", required=False, max_length=500)
    imdb = forms.CharField(label="IMDB Link", required=False, max_length=500)
    bio = forms.CharField(label="Bio", required=False, max_length=1000)

class CreateEventForm(BaseForm):
    eventID = forms.CharField(widget=forms.HiddenInput, required=False, max_length=10)
    poster = forms.CharField(widget=forms.HiddenInput, required=False, max_length=200)
    eventPicturePath = forms.CharField(widget=forms.HiddenInput, required=False)
    eventPicture = forms.FileField(label="New event picture", required=False)
    title = forms.CharField(label="Title", required=True, max_length=500)
    description = forms.CharField(label="Event Description", required=True, max_length=5000)
    location = forms.CharField(label="Location", required=True, max_length=1000)
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))

