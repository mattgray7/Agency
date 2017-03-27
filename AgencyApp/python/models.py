from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserAccount(models.Model):
	email = models.EmailField(max_length=100)
	username = models.CharField(max_length=100)

	def __str__(self):
		return self.username

class Posting(models.Model):
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.description