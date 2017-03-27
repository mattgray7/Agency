from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserAccount(models.Model):
	email = models.EmailField(max_length=100)
	username = models.CharField(max_length=10)
	setupComplete = models.BooleanField(default=False)
	workInterest = models.BooleanField(default=False)
	crewInterest = models.BooleanField(default=False)
	collaborationInterest = models.BooleanField(default=False)
	profilePicture = models.FileField(default='')

	#TODO use FileField
	reelLink = models.CharField(max_length=500, default='')
	imdbLink = models.CharField(max_length=500, default='')
	bio = models.CharField(max_length=1000, default='')

	def __str__(self):
		return self.username

class Professions(models.Model):
	#TODO Use lists?
	username = models.CharField(max_length=100)
	actor = models.BooleanField(default=False)
	director = models.BooleanField(default=False)
	writer = models.BooleanField(default=False)
	cinematographer = models.BooleanField(default=False)
	other = models.CharField(default='', max_length=200)

class Posting(models.Model):
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.description