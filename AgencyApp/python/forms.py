from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
    loginSource = forms.CharField(widget=forms.HiddenInput, required=False)

class CreateAccountForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput)
    firstName = forms.CharField(label="First Name", max_length=50)
    lastName = forms.CharField(label="Last Name", max_length=50)

class SelectInterestsForm(forms.Form):
	work = forms.BooleanField(label="Work", required=False)
	crew = forms.BooleanField(label="Crew", required=False)
	collaboration = forms.BooleanField(label="Collaboration", required=False)

class SelectProfessionsForm(forms.Form):
	actor = forms.BooleanField(label="Actor", required=False)
	director = forms.BooleanField(label="Director", required=False)
	writer = forms.BooleanField(label="Writer", required=False)
	cinematographer = forms.BooleanField(label="Cinematographer", required=False)
	other = forms.CharField(label="Other", required=False, max_length=200)

class AddBackgroundForm(forms.Form):
	profilePicture = forms.FileField(label="Profile Picture", required=False)
	reel = forms.CharField(label="Reel Link", required=False, max_length=500)
	imdb = forms.CharField(label="IMDB Link", required=False, max_length=500)
	bio = forms.CharField(label="Bio", required=False, max_length=1000)