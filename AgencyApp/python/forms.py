from django import forms
from models import *
from constants import *
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

class EditInterestsForm(forms.Form):
	work = forms.BooleanField(label="Work", required=False)
	crew = forms.BooleanField(label="Crew", required=False)
	collaboration = forms.BooleanField(label="Collaboration", required=False)
	source = forms.CharField(widget=forms.HiddenInput, required=False)
	editSource = forms.CharField(widget=forms.HiddenInput, required=False)

class EditProfessionsForm(forms.Form):
    professions = forms.MultipleChoiceField(choices=[(x, x) for x in PROFESSIONS] , widget=forms.CheckboxSelectMultiple)
    source = forms.CharField(widget=forms.HiddenInput, required=False)
    editSource = forms.CharField(widget=forms.HiddenInput, required=False)

from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.html import escape, conditional_escape

class Select(forms.Select):
    """
    A subclass of Select that adds the possibility to define additional 
    properties on options.

    It works as Select, except that the ``choices`` parameter takes a list of
    3 elements tuples containing ``(value, label, attrs)``, where ``attrs``
    is a dict containing the additional attributes of the option.
    """
    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label, attrs):
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            attrs_html = []
            for k, v in attrs.items():
                attrs_html.append('%s="%s"' % (k, escape(v)))
            if attrs_html:
                attrs_html = " " + " ".join(attrs_html)
            else:
                attrs_html = ""
            return u'<option value="{0}"{1}{2}>{3}</option>'.format(
                escape(option_value), selected_html, attrs_html, 
                conditional_escape(force_unicode(option_label))
                )
            '''
            return u'<option value="%s"%s%s>%s</option>' % (
                escape(option_value), selected_html, attrs_html,
                conditional_escape(force_unicode(option_label)))
            '''
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label, option_attrs in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(render_option(*option))
                output.append(u'</optgroup>')
            else:
                output.append(render_option(option_value, option_label,
                    option_attrs))
        return u'\n'.join(output)

class ProForm2(forms.ModelMultipleChoiceField):
    print dir(forms)
    professions = forms.ModelChoiceField(queryset=Profession.objects.filter(username=User.objects.get()),
        widget=forms.CheckboxSelectMultiple())
    APPROVAL_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('cancelled', 'Cancelled'),
)


    class Meta:
        model = Profession
        fields = ["professions"]

    def __init__(self, *args, **kwargs):
        super(ProForm2, self).__init__(*args, **kwargs)
        print "set approval choices"
        # add your relevant conditions that determines the approval choice
        # if you want to be able to modift the APPROVAL_CHOICES, change it 
        # to a list rather than a tuple
        # else
        approval_choices = self.APPROVAL_CHOICES
        self.fields['professions'].choices = approval_choices


class ProForm(forms.SelectMultiple, Select):
    print "matching professions: {0}".format(Profession.objects.filter(username=User.objects.get()))
    options = [(x,x) for x in Profession.objects.filter(username=User.objects.get())]
    print "here"
    professions = forms.MultipleChoiceField(choices=[(x, x) for x in PROFESSIONS], widget=forms.CheckboxSelectMultiple())

    source = forms.CharField(widget=forms.HiddenInput, required=False)
    editSource = forms.CharField(widget=forms.HiddenInput, required=False)
    

class EditProfessionsForm(forms.Form):
    professions = forms.ModelChoiceField(queryset=MasterProfession.objects.all(), widget=forms.CheckboxSelectMultiple(),
                                         initial=PROFESSIONS[0])
    source = forms.CharField(widget=forms.HiddenInput, required=False)
    editSource = forms.CharField(widget=forms.HiddenInput, required=False)
    def __init__(self, *args, **kwargs):
        super(EditProfessionsForm, self).__init__(*args, **kwargs)

class EditPictureForm(forms.Form):
	profilePicture = forms.FileField(label="Profile Picture")
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
