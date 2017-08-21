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
    profilePicture = forms.FileField(label="Add picture", required=False)

class EditBackgroundForm(BaseForm):
    mainProfession = forms.CharField(label="Primary Profession", required=False, max_length=200)
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
    status = forms.CharField(widget=forms.HiddenInput, max_length=50, required=False)
    description = forms.CharField(label="Description*", required=True, max_length=5000)

class CreateEventPostForm(GenericCreatePostForm):
    location = forms.CharField(label="Location", required=True, max_length=1000)
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))

class CreateProjectPostForm(GenericCreatePostForm):
    projectType = forms.CharField(label="Project Type", max_length=200)
    length = forms.CharField(label="Project Length", max_length=200, required=False)      # only filled if status is Filled (vs Hiring)
    union = forms.BooleanField(label="Union Affiliated", required=False)
    location = forms.CharField(label="Location*", max_length=200)
    shortDescription = forms.CharField(label="Short Description*", max_length=200)

class CreateCollaborationPostForm(GenericCreatePostForm):
    collaboratorRole = forms.CharField(widget=forms.HiddenInput, max_length=200, required=True)

class CreateWorkPostForm(GenericCreatePostForm):
    profession = forms.CharField(max_length=200, required=True)
    paid = forms.BooleanField(label="Paid", required=False)
    postID = forms.CharField(widget=forms.HiddenInput, max_length=10)
    projectID = forms.CharField(widget=forms.HiddenInput, required=False, max_length=10)
    poster = forms.CharField(widget=forms.HiddenInput, max_length=200)
    postPicturePath = forms.CharField(widget=forms.HiddenInput, required=False)
    postPicture = forms.ImageField(label="Picture", required=False)
    title = forms.CharField(label="Post Title*", max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder': 'Looking for Camera Operator'}))
    status = forms.CharField(label="Job Status*", widget=forms.HiddenInput, max_length=50, required=False)
    shortDescription = forms.CharField(label="Short Description*", widget=forms.TextInput(attrs={'placeholder': 'Basic single camera work on tv show'}), max_length=200, required=True)
    description = forms.CharField(label="Description*", widget=forms.TextInput(attrs={'placeholder': 'The hiree must be able to handle all camera operations for all set days. They will be compensated at an hourly rate, with potential for reshoots after primary production.'}), required=True, max_length=5000)
    paid = forms.BooleanField(label="Paid", required=False)
    paidDescription = forms.CharField(label="Specify", max_length=100, required=False)
    workerName = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)      # only filled if Cast
    skills = forms.CharField(label="Required Skills", max_length=300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Knowledge of Canon Rebel T series or Nikon D3000 series a plus.'}))
    startDate = forms.DateField(label="Start Date*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    endDate = forms.DateField(label="End Date*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    hoursPerWeek = forms.CharField(label="Hours Per Week", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'TBD'}))
    location = forms.CharField(label="Location", max_length=300, required=False, widget=forms.TextInput(attrs={'placeholder': 'UBC Campus'}))
    workerNeedsEquipment = forms.BooleanField(label="Must Provide Equipment", required=False)
    equipmentDescription = forms.CharField(label="Equipment List", widget=forms.TextInput(attrs={'placeholder': 'Camera, Tripod, Shade, All necessary lighting equipment'}), required=False, max_length=300)

class CreateCastingPostForm(BaseForm):
    postID = forms.CharField(widget=forms.HiddenInput, max_length=10)
    projectID = forms.CharField(widget=forms.HiddenInput, required=False, max_length=10)
    poster = forms.CharField(widget=forms.HiddenInput, max_length=200)
    postPicturePath = forms.CharField(widget=forms.HiddenInput, required=False)
    postPicture = forms.ImageField(label="Picture", required=False)
    title = forms.CharField(label="Post Title*", max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder': 'Looking for lead male'}))
    characterName = forms.CharField(label="Character Name*", widget=forms.TextInput(attrs={'placeholder': 'John Smith'}), max_length=200, required=True)
    characterType = forms.CharField(label="Role Type*", max_length=100, required=True)
    status = forms.CharField(label="Role Status*", widget=forms.HiddenInput, max_length=50, required=False)
    location = forms.CharField(label="Location*", widget=forms.TextInput(attrs={'placeholder': 'Metro Vancouver'}), max_length=1000, required=True)
    description = forms.CharField(label="Description*", widget=forms.TextInput(attrs={'placeholder': 'John is a charismatic father of 2 who loves his dogs.'}), required=True, max_length=5000)
    compensationType = forms.CharField(label="Compensation", required=False)
    compensationDescription = forms.CharField(widget=forms.HiddenInput, max_length=100, required=False)
    actorName = forms.CharField(widget=forms.HiddenInput, max_length=200, required=False)      # only filled if Cast
    hairColor = forms.CharField(label="Hair Color", max_length=50, required=False)
    eyeColor = forms.CharField(label="Eye Color", max_length=50, required=False)
    ethnicity = forms.CharField(label="Ethnicity", max_length=50, required=False)
    ageRange = forms.CharField(label="Age Range", max_length=50, required=False)
    gender = forms.CharField(label="Identified Gender", max_length=50, required=False)
    build = forms.CharField(label="Build", max_length=50, required=False)
    height = forms.CharField(label="Height", max_length=50, required=False)
    skills = forms.CharField(label="Required Skills", max_length=300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Stage combat, Singing, and Basketball'}))
    languages = forms.CharField(label="Languages ", max_length=300, required=False, widget=forms.TextInput(attrs={'placeholder': '(excluding English)'}))
    startDate = forms.DateField(label="Start Date*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    endDate = forms.DateField(label="End Date*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    hoursPerWeek = forms.CharField(label="Hours Per Week", max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'TBD'}))

class CreateEventPostForm(BaseForm):
    postID = forms.CharField(widget=forms.HiddenInput, max_length=10)
    projectID = forms.CharField(widget=forms.HiddenInput, required=False, max_length=10)
    poster = forms.CharField(widget=forms.HiddenInput, max_length=200)
    postPicture = forms.ImageField(label="Picture", required=False)
    title = forms.CharField(label="Event Name*", max_length=500, required=True, widget=forms.TextInput(attrs={'placeholder': 'Open Casting Call'}))
    status = forms.CharField(widget=forms.HiddenInput, max_length=50, required=False)
    location = forms.CharField(label="Location*", max_length=1000, required=True, widget=forms.TextInput(attrs={'placeholder': 'The Orpheum, 601 Smithe St, Vancouver, BC V6B 3L4'}))
    date = forms.DateField(label="Date*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    startTime = forms.TimeField(label="Start Time*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    endTime = forms.TimeField(label="End Time*", required=False, widget=forms.DateInput(attrs={'class':'datepicker'}))
    host = forms.CharField(label="Hosted by", required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Matthew Gray, Amy Bolt'}))
    description = forms.CharField(label="Description*", widget=forms.TextInput(attrs={'placeholder': 'Casting multiple minor roles for The Greate Gatsby. All actors, male and female, of all ages are welcome.'}), required=True, max_length=5000)
    admissionInfo = forms.CharField(label="Admission", required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Open to public'}))

