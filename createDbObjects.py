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

print "\nDeleting media..."
os.system("rm -r /Users/MattGray/Projects/Agency/Agency/media/*")

print "\nCreating new user network.\n"

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
                             		imdbLink="http://www.imdb.com/name/nm6547223/?ref_=ttfc_fc_cl_t47",
                             		bio="I love dogs, films, and video games.",
                             		mainProfession="Cinematographer")
os.makedirs("/Users/MattGray/Projects/Agency/Agency/media/mattgray/")
picResult = urllib.urlretrieve("/Users/MattGray/Projects/Agency/Agency/scripts/media/mattGrayProfile.jpg")
project1UserAccount.profilePicture = File(open(picResult[0]))
project1UserAccount.profilePicture.name = "/profile.jpg"
project1UserAccount.save()


def createProject(poster, title, description, status, picURL):
	projectID = helpers.createUniqueID(models.ProjectPost, "postID")
	projectPost = models.ProjectPost(postID=projectID,
									 projectID=projectID,
									 poster=poster,
									 title=title,
									 description=description,
									 status=status)
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		projectPost.postPicture = File(open(picResult[0]))
		projectPost.postPicture.name = "/project_{0}.jpg".format(projectID)
	projectPost.save()
	return projectPost

# Great Gatsby project
project1ProjectPost = createProject(poster="mattgray",
									title="The Great Gatsby",
									description="The Great Gatsby follows Fitzgerald-like, would-be writer Nick Carraway (Tobey Maguire) as he leaves the Midwest and comes to New York City in the spring of 1922, an era of loosening morals, glittering jazz and bootleg kings. Chasing his own American Dream, Nick lands next door to a mysterious, party-giving millionaire, Jay Gatsby (Leonardo DiCaprio) and across the bay from his cousin, Daisy (Carey Mulligan) and her philandering, blue-blooded husband, Tom Buchanan (Joel Edgerton).",
									status="In production",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/greatGatsby.jpg")
project1ProjectID = project1ProjectPost.projectID


project2ProjectPost = createProject(poster="mattgray",
									title="The Kings of Summer",
									description="Three kids build a house in the woods and run away from their families",
									status="Completed",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/kingsOfSummer.jpg")

project3ProjectPost = createProject(poster="mattgray",
									title="Valerian",
									description="A space opera from Luc Besson based on the legendary French comic books.",
									status="Pre-production",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/valerian.jpg")

project4ProjectPost = createProject(poster="mattgray",
									title="There Will Be Blood",
									description="A study of a man obsessed with power during the oil boom.",
									status="Completed",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/thereWillBeBlood.jpg")

project5ProjectPost = createProject(poster="mattgray",
									title="Arrival",
									description="As an alien ship appears on Earth, one cunning linguist may be our only hope of survival.",
									status="Completed",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/arrival.jpg")

project6ProjectPost = createProject(poster="mattgray",
									title="Fantastic Beasts and Where To Find Them",
									description="Newt Scamander must wrangle mythical beasts in 1920s New York in this Harry Potter spinoff.",
									status="Post production",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/fantasticBeasts.jpg")

project7ProjectPost = createProject(poster="johnstongray",
									title="Reel Adults",
									description="James, a film school drop out and his best friend Tyson embark on a fucking crazy journey as they make their FIRST FEATURE FILM!!!",
									status="Completed",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/reelAdults.jpg")


def createProjectJob(projectID, username, status, profession, title, description, paid, picURL=None):
	jobID = helpers.createUniqueID(models.ProjectJob, "postID")

	projectJob = models.ProjectJob(postID=jobID, projectID=projectID, status=status,
								   username=username, profession=profession)
	projectJob.save()

	jobPost = models.WorkPost(postID=jobID, projectID=projectID, poster=username,
							  title=title, description=description, paid=paid, profession=profession,
							  status=status)
	jobPost.save()
	return jobID

def createProjectRole(projectID, username, status, title, characterName, paid, shortCharacterDescription=None, characterDescription=None, picURL=None):
	roleID = helpers.createUniqueID(models.ProjectRole, "postID")
	projectRole = models.ProjectRole(postID=roleID, projectID=projectID, status=status,
								   	 username=username, characterName=characterName, 
								   	 characterDescription=characterDescription, shortCharacterDescription=shortCharacterDescription)
	projectRole.save()
	"""TODO should not have poster as username when I fix the post system"""
	rolePost = models.CastingPost(postID=roleID, projectID=projectID, poster=username,
								  title=title, description=characterDescription, paid=paid,
								  status=status)
	rolePost.save()
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		rolePost.postPicture = File(open(picResult[0]))
		rolePost.postPicture.name = "/casting_{0}.jpg".format(roleID)
		rolePost.save()
	return roleID

project1WorkPost2JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="mattgray",
								 		  title="Director Needed",
								 		  description="Head of production",
								 		  paid=True,
								 		  profession="Director",
								 		  status="Filled")
project1WorkPost3JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="amybolt",
								 		  title="Co-Director Needed",
								 		  description="Head of directing",
								 		  paid=True,
								 		  profession="Director",
								 		  status="Filled")
project1WorkPost4JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="adamcramer",
								 		  title="SFX Heavy show, need supervisor",
								 		  description="Head/Producer of SFX",
								 		  paid=True,
								 		  profession="Producer",
								 		  status="Filled")
project1WorkPost5JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="amybolt",
								 		  title="Screenwriter wanted",
								 		  description="I need someone to write this script from my idea",
								 		  paid=True,
								 		  profession="Screenwriter",
								 		  status="Filled")
project1WorkPost6RoleId = createProjectRole(projectID=project1ProjectID,
								 		    username="liamcarson",
								 		    title="Male lead needed",
								 		    characterName="Nick Carraway",
								 		    characterDescription="A guy that gets taken in by this rich guy and then some stuff happens idk I kind of forget the book it was so long ago.",
								 		    shortCharacterDescription="24-30 innocent looking male, he should be soft spoken and calm",
								 		    paid=True,
								 		    status="Cast",
								 		    picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/nickCarraway.png")

project1WorkPost7RoleId = createProjectRole(projectID=project1ProjectID,
								 		    username="sachahusband",
								 		    title="Male lead needed",
								 		    characterName="Jay Gatsby",
								 		    characterDescription='The guy that the book is named after, so he must be kinf od important right. That makes sense. Anyways, he is rich and you should look like you are.',
								 		    shortCharacterDescription="Lead male aged 40-50",
								 		    paid=True,
								 		    status="Cast",
								 		    picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/jayGatsby.jpg")

project1WorkPost8RoleId = createProjectRole(projectID=project1ProjectID,
								 		    username="amybolt",
								 		    title="Female lead",
								 		    characterName="Daisy Buchanan",
								 		    characterDescription="This chick is like so random its ridiculous. wow weird, i have run out of things to think of.",
								 		    shortCharacterDescription="Mid-20s brunette female lead",
								 		    paid=True,
								 		    status="Cast",
								 		    picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/daisyBuchanan.png")

project1RoleId2 = createProjectRole(projectID=project1ProjectID,
								 	username="mattgray",
								 	title="Looking for young 20-something male to play a random guy",
								 	characterName="Clark",
								 	characterDescription="Looks like he comes from a wealthy family",
								 	paid=True,
								 	status="Open")
project1RoleId2 = createProjectRole(projectID=project1ProjectID,
								 	username="mattgray",
								 	title="Looking for young 20-something female to play a random guy's gf",
								 	characterName="Mona Lisa Saperstein",
								 	characterDescription = "She is the worst. It is unbelievable how bad she is. She is the brother of jean rakphio saperstein, so actress must look related.",
								 	shortCharacterDescription="She is the wooooooooooorst",
								 	paid=True,
								 	status="Open")

project2JobId = createProjectJob(projectID=project7ProjectPost.projectID,
								 		    username="johnstongray",
								 		    title="Creator",
								 		    description="I wrote the whole thing",
								 		    paid=True,
								 		    profession="Director",
								 		    status="Filled")

project2RoleId = createProjectRole(projectID=project7ProjectPost.projectID,
								 	username="johnstongray",
								 	title="blah",
								 	characterName="James",
								 	characterDescription="Own the room",
								 	paid=True,
								 	status="Cast")

project2JobID = createProjectJob(projectID=project1ProjectID,
								 		  username="adamcramer",
								 		  title="SFX Heavy show, need supervisor",
								 		  description="Head/Producer of SFX",
								 		  paid=True,
								 		  profession="Producer",
								 		  status="Filled")



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
project1WorkPost.postPicture.name = "/work_{0}.jpg".format(project1WorkPostID)
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
project1EventPost.postPicture.name = "/event_{0}.jpg".format(project1EventPostID)
project1EventPost.save()

# ====================
def createUser(username, email, password, firstName, lastName, picURL=None):
	user = User.objects.create_user(username=username,
                                   	email=email,
                                   	password=password,
                                   	first_name=firstName,
                                   	last_name=lastName)
	user.save()
	userAccount = models.UserAccount(username=username,
								 		email=email,
	                             		firstName=firstName,
	                             		lastName=lastName,
	                             		setupComplete=True)
	userAccount.save()
	userMediaDir = "/Users/MattGray/Projects/Agency/Agency/media/{0}/".format(username)
	if not os.path.exists(userMediaDir):
		os.makedirs(userMediaDir)
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		userAccount.profilePicture = File(open(picResult[0]))
		userAccount.profilePicture.name = "/profile.jpg"
		userAccount.save()

# Add more user stuff
# User 2
user2 = createUser("amybolt", "amy.bolt@hotmail.com", "m", "amy", "bolt",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/amyBoltProfile.jpg")
user3 = createUser("adamcramer", "adam.cramos@gmail.com", "m", "adam", "cramer",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/adamCramerProfile.jpg")
user4 = createUser("johnstongray", "johnston.gray@gmail.com", "m", "johnston", "gray",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/johnstonGrayProfile.jpg")
user5 = createUser("sachahusband", "sasha.husband@gmail.com", "m", "sasha", "husband",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/sachaHusbandProfile.jpg")
user6 = createUser("liamcarson", "liam.carson@gmail.com", "m", "liam", "carson")
				   #"/Users/MattGray/Projects/Agency/Agency/scripts/media/liamCarsonProfile.jpg")

# Add some professions
professionList = [models.Interest(username="mattgray", mainInterest="work", subInterest="onSetProduction", professionName="Cinematographer"),
				  models.Interest(username="mattgray", mainInterest="work", subInterest="preProduction", professionName="Choreographer"),
				  models.Interest(username="mattgray", mainInterest="work", subInterest="postProduction", professionName="VFX Artist"),
				  models.Interest(username="mattgray", mainInterest="work", subInterest="preProduction", professionName="Screenwriter"),
				  models.Interest(username="amybolt", mainInterest="work", subInterest="acting", professionName="Dancer"),
				  models.Interest(username="amybolt", mainInterest="work", subInterest="creative", professionName="Songwriter"),
				  models.Interest(username="amybolt", mainInterest="work", subInterest="onSetProduction", professionName="Photographer"),
				  models.Interest(username="amybolt", mainInterest="work", subInterest="offSetProduction", professionName="Production Coordinator"),
				  models.Interest(username="adamcramer", mainInterest="work", subInterest="onSetProduction", professionName="SFX Technician"),
				  models.Interest(username="adamcramer", mainInterest="work", subInterest="onSetProduction", professionName="SFX Supervisor"),
				  models.Interest(username="johnstongray", mainInterest="work", subInterest="onSetProduction", professionName="Cinematographer"),
				  models.Interest(username="johnstongray", mainInterest="work", subInterest="acting", professionName="Actor"),
				  models.Interest(username="johnstongray", mainInterest="work", subInterest="onSetProduction", professionName="Set Decorator"),
				  models.Interest(username="johnstongray", mainInterest="work", subInterest="creative", professionName="Screenwriter"),
				  models.Interest(username="johnstongray", mainInterest="work", subInterest="creative", professionName="Director"),
				  models.Interest(username="liamcarson", mainInterest="work", subInterest="acting", professionName="Model"),
				  models.Interest(username="sachahusband", mainInterest="work", subInterest="creative", professionName="Screenwriter"),
				  models.Interest(username="sachahusband", mainInterest="work", subInterest="creative", professionName="Director"),
				  models.Interest(username="sachahusband", mainInterest="work", subInterest="creative", professionName="Director of Photography")]
for profession in professionList:
	profession.save()


# Add follows
postFollow = models.PostFollow(postID=project1EventPostID, username="amybolt")
postFollow.save()
postFollow = models.PostFollow(postID=project1ProjectID, username="amybolt")
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
collabPost.postPicture.name = "/collaboration_{0}.jpg".format(collabPostID)
collabPost.save()

