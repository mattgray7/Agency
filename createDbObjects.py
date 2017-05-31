import os
import datetime
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Agency.settings")
django.setup()

from django.contrib.auth.models import User
import AgencyApp.python.models as models
import AgencyApp.python.helpers as helpers

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
                             		setupComplete=True)
project1UserAccount.save()


# User 2
project1User2 = User.objects.create_user(username="amybolt",
                                   email="amy.bolt@hotmail.com",
                                   password="m",
                                   first_name="amy",
                                   last_name="bolt")
project1User2.save()
project1UserAccount2 = models.UserAccount(username="amybolt",
							 		email="amy.bolt@hotmail.com",
                             		firstName="amy",
                             		lastName="bolt",
                             		setupComplete=True)
project1UserAccount2.save()

# Great Gatsby project
project1ProjectID = helpers.createUniqueID(models.ProjectPost, "postID")
project1ProjectPost = models.ProjectPost(postID=project1ProjectID,
									poster="mattgray",
									title="The Great Gatsby",
									description="Modern reimagining set in project1 York",
									status="In production")
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
project1CastingPost2.save()

# Daisy Buchanen casting post
project1CastingPostID3 = helpers.createUniqueID(models.CastingPost, "postID")
project1CastingPost3 = models.CastingPost(postID=project1CastingPostID3,
									projectID=project1ProjectID,
									poster="mattgray",
									title="Daisy Buchanen",
									description="Mid-20s brunette female lead",
									status="Open",
									paid=True)
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
project1EventPost.save()