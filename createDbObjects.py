import os
import urllib
import datetime
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Agency.settings")
django.setup()

from django.contrib.auth.models import User
from django.core.files import File
import AgencyApp.python.helpers as helpers
import AgencyApp.python.models as models


print "Flushing database..."
os.system("python /Users/MattGray/Projects/Agency/Agency/manage.py flush")

#=================== Project 1
# User 1
project1User = User.objects.create_user(username="mattgray",
                                   email="matt.gray.1993@gmail.com",
                                   password="m",
                                   first_name="matt",
                                   last_name="gray")
project1User.save()
project1UserAccount = models.UserAccount(username="mattgray",
							 		email="matt.gray.1993@gmail.com",
                             		firstName="matt",
                             		lastName="gray",
                             		setupComplete=True,
                             		crewInterest=True,
                             		castingInterest=True,
                             		workInterest=True,
                             		actingInterest=True,
                             		collaborationInterest=True)
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/mattGrayProfile.jpg")
project1UserAccount.profilePicture = File(open(picResult[0]))
project1UserAccount.save()


# Great Gatsby project
project1ProjectID = helpers.createUniqueID(models.ProjectPost, "postID")
project1ProjectPost = models.ProjectPost(postID=project1ProjectID,
									poster="mattgray",
									title="The Great Gatsby",
									description="Modern reimagining set in New York",
									status="In production")
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/greatGatsby.jpg")
project1ProjectPost.postPicture = File(open(picResult[0]))
project1ProjectPost.save()


# Nick Carraway casting post
project1CastingPostID = helpers.createUniqueID(models.CastingPost, "postID")
project1CastingPost = models.CastingPost(postID=project1CastingPostID,
									projectID=project1ProjectID,
									poster="mattgray",
									title="Nick Carraway",
									description="Young male lead",
									status="Open",
									paid=True)
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/nickCarraway.png")
project1CastingPost.postPicture = File(open(picResult[0]))
project1CastingPost.save()


# Jay Gatsby casting post
project1CastingPostID2 = helpers.createUniqueID(models.CastingPost, "postID")
project1CastingPost2 = models.CastingPost(postID=project1CastingPostID2,
									projectID=project1ProjectID,
									poster="mattgray",
									title="Jay Gatsby",
									description="Middle-aged male lead",
									status="Open",
									paid=True)
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/jayGatsby.jpg")
project1CastingPost2.postPicture = File(open(picResult[0]))
project1CastingPost2.save()


# Daisy Buchanen casting post
project1CastingPostID3 = helpers.createUniqueID(models.CastingPost, "postID")
project1CastingPost3 = models.CastingPost(postID=project1CastingPostID3,
									projectID=project1ProjectID,
									poster="mattgray",
									title="Daisy Buchanan",
									description="Mid-20s brunette female lead",
									status="Open",
									paid=True)
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/daisyBuchanan.png")
project1CastingPost3.postPicture = File(open(picResult[0]))
project1CastingPost3.save()


# Photographer job post
project1WorkPostID = helpers.createUniqueID(models.WorkPost, "postID")
project1WorkPost = models.WorkPost(postID=project1WorkPostID,
								 projectID=project1ProjectID,
								 poster="mattgray",
								 title="Stills photographer needed",
								 description="3 days on set",
								 paid=True,
								 profession="Photographer",
								 status="Hiring")
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/photographer.jpg")
project1WorkPost.postPicture = File(open(picResult[0]))
project1WorkPost.save()


# Open table read event
project1EventPostID = helpers.createUniqueID(models.EventPost, "postID")
project1EventPost = models.EventPost(postID=project1EventPostID,
								 projectID=project1ProjectID,
								 poster="mattgray",
								 title="Open casting call",
								 description="Casting for all roles",
								 location="Hyatt Vancouver",
								 date=datetime.datetime(2017, 06, 02))
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/castingCall.jpeg")
project1EventPost.postPicture = File(open(picResult[0]))
project1EventPost.save()

# ====================


# Add more user stuff
# User 2
user2 = User.objects.create_user(username="amybolt",
                                   email="amy.bolt@hotmail.com",
                                   password="m",
                                   first_name="amy",
                                   last_name="bolt")
user2.save()
userAccount2 = models.UserAccount(username="amybolt",
							 		email="amy.bolt@hotmail.com",
                             		firstName="amy",
                             		lastName="bolt",
                             		actingInterest=True,
                             		collaborationInterest=True,
                             		workInterest=True,
                             		setupComplete=True)
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/amyBoltProfile.jpg")
userAccount2.profilePicture = File(open(picResult[0]))
userAccount2.save()

# Add some professions
professionList = [models.Profession(username="mattgray", professionName="Cinematographer"),
				  models.Profession(username="mattgray", professionName="Photographer"),
				  models.Profession(username="mattgray", professionName="VFX Artist"),
				  models.Profession(username="mattgray", professionName="Writer"),
				  models.Profession(username="amybolt", professionName="Dancer"),
				  models.Profession(username="amybolt", professionName="Songwriter"),
				  models.Profession(username="amybolt", professionName="Photographer"),
				  models.Profession(username="amybolt", professionName="Set designer")]
for profession in professionList:
	profession.save()


# Add follows
postFollow = models.PostFollow(postID=project1EventPostID, username="amybolt")
postFollow.save()
postFollow = models.PostFollow(postID=project1ProjectID, username="amybolt")
postFollow.save()
postFollow = models.PostFollow(postID=project1CastingPostID3, username="amybolt")
postFollow.save()


# Collaborator post
collabPostID = helpers.createUniqueID(models.CollaborationPost, "postID")
collabPost = models.CollaborationPost(postID=collabPostID,
								 projectID=project1ProjectID,
								 poster="amybolt",
								 title="The Yosemite Project",
								 description="I wrote a sick screenplay and am looking for a director",
								 collaboratorRole="Director")
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/collabPost.jpg")
collabPost.postPicture = File(open(picResult[0]))
collabPost.save()

