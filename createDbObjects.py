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

print "\nCopying default images to media"
defaultImagesDir = "/Users/MattGray/Projects/Agency/Agency/media/default/"
if not os.path.exists(defaultImagesDir):
	os.makedirs(defaultImagesDir)
os.system("cp /Users/MattGray/Projects/Agency/Agency/AgencyApp/static/AgencyApp/css/images/default/* {0}".format(defaultImagesDir))

print "\nCreating new user network.\n"


daisyBuchananDescription = """Daisy is The Great Gatsby's most enigmatic, and perhaps most disappointing, character. Although Fitzgerald does much to make her a character worthy of Gatsby's unlimited devotion, in the end she reveals herself for what she really is. Despite her beauty and charm, Daisy is merely a selfish, shallow, and in fact, hurtful, woman. Gatsby loves her (or at least the idea of her) with such vitality and determination that readers would like, in many senses, to see her be worthy of his devotion. Although Fitzgerald carefully builds Daisy's character with associations of light, purity, and innocence, when all is said and done, she is the opposite from what she presents herself to be. From Nick's first visit, Daisy is associated with otherworldliness. Nick calls on her at her house and initially finds her (and Jordan Baker, who is in many ways an unmarried version of Daisy) dressed all in white, sitting on an "enormous couch . . . buoyed up as though upon an anchored balloon . . . [her dress] rippling and fluttering as if [she] had just been blown back in after a short flight around the house." From this moment, Daisy becomes like an angel on earth. She is routinely linked with the color white (a white dress, white flowers, white car, and so on), always at the height of fashion and addressing people with only the most endearing terms. She appears pure in a world of cheats and liars. Given Gatsby's obsession with Daisy and the lengths to which he has gone to win her, she seems a worthy paramour."""
directorDescription = """Our vision is to change the way the world views productivity. We want Function Point to be a place where everyone feels respected, where they are doing important work and where everyone contributes to the growth and direction of our company, our customers and our community. Function Point is looking for a hands on, curious technology leader who wants to keep their technical skills sharp and apply their passion and smarts to lead engineering and devops towards delivering customer and business value. As Director of Engineering, you will work closely with our Director of Products to drive the development of Function Points products and services. You will lead the continued growth of engineering and devops with an emphasis on championing a strong engineering culture, measuring and increasing delivery velocity, ensuring high quality, and achieving schedule predictability."""
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

def createProjectAdmin(projectID, username):
	newAdmin = models.ProjectAdmin(projectID=projectID, username=username)
	newAdmin.save()
	newAdmin = models.PostAdmin(postID=projectID, username=username)
	newAdmin.save()

# Great Gatsby project
project1ProjectPost = createProject(poster="mattgray",
									title="The Great Gatsby",
									description="The Great Gatsby follows Fitzgerald-like, would-be writer Nick Carraway (Tobey Maguire) as he leaves the Midwest and comes to New York City in the spring of 1922, an era of loosening morals, glittering jazz and bootleg kings. Chasing his own American Dream, Nick lands next door to a mysterious, party-giving millionaire, Jay Gatsby (Leonardo DiCaprio) and across the bay from his cousin, Daisy (Carey Mulligan) and her philandering, blue-blooded husband, Tom Buchanan (Joel Edgerton).",
									status="In production",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/greatGatsby.jpg")
project1ProjectID = project1ProjectPost.projectID
project1Admin = createProjectAdmin(project1ProjectID, "mattgray")
project1Admin2 = createProjectAdmin(project1ProjectID, "amybolt")
project1Admin3 = createProjectAdmin(project1ProjectID, "adamcramer")

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


def createProjectJob(projectID, username, status, profession, title, paid, shortDescription=None, description=None, picURL=None, poster="mattgray"):
	jobID = helpers.createUniqueID(models.WorkPost, "postID")
	jobPost = models.WorkPost(postID=jobID, projectID=projectID, poster=poster, workerName=username, shortDescription=shortDescription,
							  title=title, description=description, paid=paid, profession=profession,
							  status=status)
	jobPost.save()

	admin = models.PostAdmin(postID=jobID, username=poster)
	admin.save()

	if picURL:
		picResult = urllib.urlretrieve(picURL)
		jobPost.postPicture = File(open(picResult[0]))
		jobPost.postPicture.name = "/work_{0}.jpg".format(jobID)
		jobPost.save()
	return jobID

def createProjectRole(projectID, username, status, title, characterName, paid, shortCharacterDescription=None, characterDescription=None, picURL=None, poster="mattgray"):
	roleID = helpers.createUniqueID(models.CastingPost, "postID")
	rolePost = models.CastingPost(title=title, postID=roleID, projectID=projectID, poster=poster, status=status,
								   	 actorName=username, characterName=characterName, 
								   	 description=characterDescription, shortCharacterDescription=shortCharacterDescription, paid=paid)
	rolePost.save()

	admin = models.PostAdmin(postID=roleID, username=poster)
	admin.save()
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		rolePost.postPicture = File(open(picResult[0]))
		rolePost.postPicture.name = "/casting_{0}.jpg".format(roleID)
		rolePost.save()
	return roleID

project1WorkPost2JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="mattgray",
								 		  title="Director Needed",
								 		  shortDescription="Need someone to oversee production and director this script.",
								 		  description=directorDescription,
								 		  paid=True,
								 		  profession="Director",
								 		  status="Filled")
project1WorkPost3JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="amybolt",
								 		  title="Co-Director Needed",
								 		  shortDescription="Head of directing",
								 		  paid=True,
								 		  profession="Director",
								 		  status="Filled")
project1WorkPost5JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="mattgray",
								 		  title="Photographer needed",
								 		  shortDescription="I need someone to shoot our set while filiming",
								 		  paid=True,
								 		  profession="Photographer",
								 		  status="Hiring",
								 		  picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/photographer.jpg")
project1WorkPost4JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="adamcramer",
								 		  title="SFX Heavy show, need supervisor",
								 		  shortDescription="Head/Producer of SFX",
								 		  paid=True,
								 		  profession="Producer",
								 		  status="Filled")
project1WorkPost5JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="amybolt",
								 		  title="Screenwriter wanted",
								 		  shortDescription="I need someone to write this script from my idea",
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
								 		    characterDescription=daisyBuchananDescription,
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
								 	status="Open",
								 	picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/randomChickDrawing.jpg")

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
