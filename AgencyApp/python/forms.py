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
    work = forms.BooleanField(label="Looking for a job", required=False)
    hire = forms.BooleanField(label="Looking to hire/cast a role", required=False)
    other = forms.BooleanField(label="Other", required=False)

class EditPictureForm(BaseForm):
    profilePicture = forms.FileField(label="New profile picture", required=False)

class EditBackgroundForm(BaseForm):
    reel = forms.CharField(label="Reel Link", required=False, max_length=500)
    imdb = forms.CharField(label="IMDB Link", required=False, max_length=500)
    bio = forms.CharField(label="Bio", required=False, max_length=1000)

class GenericCreatePostForm(BaseForm):
    postID = forms.CharField(widget=forms.HiddenInput, required=False, max_length=10)
    projectID = forms.CharField(widget=forms.HiddenInput, required=False, max_length=10)
    poster = forms.CharField(widget=forms.HiddenInput, required=False, max_length=200)
    postPicturePath = forms.CharField(widget=forms.HiddenInput, required=False)
    postPicture = forms.ImageField(label="Picture", required=False)
    title = forms.CharField(label="Title", max_length=500, required=True)
    description = forms.CharField(label="Description", required=True, max_length=5000)
    status = forms.CharField(widget=forms.HiddenInput, max_length=50, required=False)

class CreateEventPostForm(GenericCreatePostForm):
    location = forms.CharField(label="Location", required=True, max_length=1000)
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))

class CreateProjectPostForm(GenericCreatePostForm):
    pass

class CreateWorkPostForm(GenericCreatePostForm):
    profession = forms.CharField(widget=forms.HiddenInput, max_length=200, required=True)
    paid = forms.BooleanField(label="Paid", required=False)

class CreateCollaborationPostForm(GenericCreatePostForm):
    collaboratorRole = forms.CharField(widget=forms.HiddenInput, max_length=200, required=True)

class CreateCastingPostForm(GenericCreatePostForm):
    paid = forms.BooleanField(label="Paid", required=False)
    descriptionEnabled = forms.BooleanField(widget=forms.HiddenInput, required=False)




