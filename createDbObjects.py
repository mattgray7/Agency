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
def createUser(username, email, password, firstName, lastName, picURL=None, mainProfession="Actor", imdbLink='None', bio="None"):
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
	                             		setupComplete=True,
	                             		imdbLink=imdbLink,
	                             		bio=bio,
	                             		mainProfession=mainProfession)
	userAccount.save()
	userMediaDir = "/Users/MattGray/Projects/Agency/Agency/media/{0}/".format(username)
	if not os.path.exists(userMediaDir):
		os.makedirs(userMediaDir)
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		userAccount.profilePicture = File(open(picResult[0]))
		userAccount.profilePicture.name = "/profile.jpg"
		userAccount.save()

project1UserAccount = createUser("mattgray", "matt.gray.1993@gmail.com", "m", "matt", "gray",
				   picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/mattGrayProfile.jpg",
				   imdbLink="http://www.imdb.com/name/nm6547223/?ref_=ttfc_fc_cl_t47",
                   bio="I love dogs, films, and video games. And buttholes.",
                   mainProfession="Actor")
user2 = createUser("amybolt", "amy.bolt@hotmail.com", "m", "amy", "bolt",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/amyBoltProfile.jpg",
				   mainProfession="Actor")
user3 = createUser("adamcramer", "adam.cramos@gmail.com", "m", "adam", "cramer",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/adamCramerProfile.jpg",
				   mainProfession="SPFX Supervisor")
user4 = createUser("johnstongray", "johnston.gray@gmail.com", "m", "johnston", "gray",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/johnstonGrayProfile.jpg",
				   mainProfession="Screenwriter")
user5 = createUser("sachahusband", "sasha.husband@gmail.com", "m", "sasha", "husband",
				   "/Users/MattGray/Projects/Agency/Agency/scripts/media/sachaHusbandProfile.jpg",
				   mainProfession="Director")
user6 = createUser("liamcarson", "liam.carson@gmail.com", "m", "liam", "carson",
				   mainProfession="Model")
				   #"/Users/MattGray/Projects/Agency/Agency/scripts/media/liamCarsonProfile.jpg")
user7 = createUser("peterm", "peter.m@gmail.com", "m", "peter", "m",
				   mainProfession="Actor")
user8 = createUser("happymuller", "happy@gmail.com", "m", "happy", "muller",
				   mainProfession="Dancer")
user9 = createUser("johnnymater", "2k@gmail.com", "m", "johnny", "mater",
				   mainProfession="Screenwriter")
user10 = createUser("jonnycarson", "jonny.carson@gmail.com", "m", "jonny", "carson",
				   mainProfession="Actor")


"""project1UserAccount = models.UserAccount(username="mattgray",
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
project1UserAccount.save()"""


def createProject(poster, title, description, status, picURL, projectType="Film - Feature", location="Vancouver"):
	projectID = helpers.createUniqueID(models.ProjectPost, "postID")
	projectPost = models.ProjectPost(postID=projectID,
									 projectID=projectID,
									 poster=poster,
									 title=title,
									 description=description,
									 status=status,
									 projectType=projectType,
									 location=location)
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		projectPost.postPicture = File(open(picResult[0]))
		projectPost.postPicture.name = "/project_{0}.jpg".format(projectID)
	projectPost.save()
	return projectPost

def createProjectAdmin(projectID, username):
	newAdmin = models.ProjectAdmin(projectID=projectID, username=username)
	newAdmin.save()
	newPart = models.PostParticipant(postID=projectID, username=username, status="Creator")
	newPart.save()
	#newAdmin = models.PostAdmin(postID=projectID, username=username)
	#newAdmin.save()

# Great Gatsby project
project1ProjectPost = createProject(poster="mattgray",
									title="The Great Gatsby",
									description="The Great Gatsby follows Fitzgerald-like, would-be writer Nick Carraway (Tobey Maguire) as he leaves the Midwest and comes to New York City in the spring of 1922, an era of loosening morals, glittering jazz and bootleg kings. Chasing his own American Dream, Nick lands next door to a mysterious, party-giving millionaire, Jay Gatsby (Leonardo DiCaprio) and across the bay from his cousin, Daisy (Carey Mulligan) and her philandering, blue-blooded husband, Tom Buchanan (Joel Edgerton).",
									status="In production",
									picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/greatGatsby.jpg")
project1ProjectID = project1ProjectPost.projectID
project1Admin = createProjectAdmin(project1ProjectID, "mattgray")
#project1Admin2 = createProjectAdmin(project1ProjectID, "amybolt")
#project1Admin3 = createProjectAdmin(project1ProjectID, "adamcramer")

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

import datetime
today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1)

def createProjectJob(projectID, status, profession, title, compensationType="Paid", compensationDescription="$100/day", username=None,description=None, picURL=None, poster="mattgray", startDate=None, endDate=None):
	jobID = helpers.createUniqueID(models.WorkPost, "postID")
	jobPost = models.WorkPost(postID=jobID, projectID=projectID, poster=poster, workerName=username,
							  title=title, description=description, compensationType=compensationType, compensationDescription=compensationDescription, profession=profession,
							  status=status, startDate=startDate or today, endDate=endDate or tomorrow)
	jobPost.save()

	admin = models.PostAdmin(postID=jobID, username=poster)
	admin.save()

	if picURL:
		picResult = urllib.urlretrieve(picURL)
		jobPost.postPicture = File(open(picResult[0]))
		jobPost.postPicture.name = "/work_{0}.jpg".format(jobID)
		jobPost.save()
	return jobID

def createProjectRole(projectID, status, title, characterName, compensationType="Paid", compensationDescription="$100/day", username=None, gender=None, location=None, characterDescription=None, picURL=None, poster="mattgray", startDate=None, endDate=None):
	roleID = helpers.createUniqueID(models.CastingPost, "postID")
	rolePost = models.CastingPost(title=title, postID=roleID, projectID=projectID, poster=poster, status=status,
								  actorName=username, characterName=characterName, gender=gender,
								  description=characterDescription, location=location,
								  compensationType=compensationType, compensationDescription=compensationDescription, startDate=startDate or today, endDate=endDate or tomorrow)
	rolePost.save()

	admin = models.PostAdmin(postID=roleID, username=poster)
	admin.save()
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		rolePost.postPicture = File(open(picResult[0]))
		rolePost.postPicture.name = "/casting_{0}.jpg".format(roleID)
		rolePost.save()
	return roleID

def createProjectEvent(projectID, title, location, startDate, endDate, startTime, endTime, description, poster="mattgray", host=None, admissionInfo=None, picURL=None):
	postID = helpers.createUniqueID(models.EventPost, "postID")
	post = models.EventPost(postID=postID,
								 projectID=projectID,
								 poster=poster,
								 title=title,
								 description=description,
								 location=location,
								 host=host,
								 admissionInfo=admissionInfo,
								 startTime=startTime,
								 endTime=endTime,
								 startDate=startDate,
								 endDate=endDate)
	post.save()
	if picURL:
		picResult = urllib.urlretrieve(picURL)
		post.postPicture = File(open(picResult[0]))
		post.postPicture.name = "/event_{0}.jpg".format(postID)
		post.save()
	return postID

project1WorkPost2JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="mattgray",
								 		  title="Director Needed",
								 		  description=directorDescription,
								 		  profession="Director",
								 		  status="Filled")
project1WorkPost3JobId = createProjectJob(projectID=project1ProjectID,
								 		  title="Co-Director Needed",
								 		  description="Head of directing",
								 		  compensationType="Negotiable",
								 		  compensationDescription="Depends on number of days worked",
								 		  profession="Director",
								 		  status="Open")
project1WorkPost4JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="mattgray",
								 		  title="Photographer needed",
								 		  description="I need someone to shoot our set while filiming",
								 		  profession="Photographer",
								 		  status="Open",
								 		  picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/photographer.jpg")
project1WorkPost5JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="adamcramer",
								 		  title="SFX Heavy show, need supervisor",
								 		  description="Head/Producer of SFX",
								 		  profession="Producer",
								 		  status="Filled")
project1WorkPost6JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="amybolt",
								 		  title="Screenwriter wanted",
								 		  compensationType="Unpaid",
								 		  profession="Screenwriter",
								 		  status="Filled")
project1WorkPost7JobId = createProjectJob(projectID=project1ProjectID,
								 		  username="amybolt",
								 		  title="Screenwriter wanted",
								 		  description="I need someone to write this script from my idea",
								 		  profession="Screenwriter",
								 		  status="Filled")
project1WorkPost7JobId = createProjectJob(projectID=project1ProjectID,
								 		  title="Key Grip",
								 		  description="Be prepared to work 12 - 16 hour days, every day of production",
								 		  profession="Key Grip",
								 		  status="Opening soon")
project1WorkPost7JobId = createProjectJob(projectID=project1ProjectID,
								 		  title="Looking for a Senior Camera Operator",
								 		  description="Primary and seconday cmaera operators",
								 		  profession="Camera Operator",
								 		  status="Opening soon")

project1RoleId1 = createProjectRole(projectID=project1ProjectID,
								 		    username="liamcarson",
								 		    title="Male lead needed",
								 		    characterName="Nick Carraway",
								 		    characterDescription="A guy that gets taken in by this rich guy and then some stuff happens idk I kind of forget the book it was so long ago. 24-30 innocent looking male, he should be soft spoken and calm",
								 		    location="UBC Campus",
								 		    status="Cast",
								 		    picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/nickCarraway.png")

project1RoleId2 = createProjectRole(projectID=project1ProjectID,
								 		    username="sachahusband",
								 		    title="Male lead needed",
								 		    characterName="Jay Gatsby",
								 		    characterDescription='The guy that the book is named after, so he must be kinf od important right. That makes sense. Anyways, he is rich and you should look like you are.',
								 		    location="UBC Campus",
								 		    compensationType="Unpaid",
								 		    status="Cast",
								 		    picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/jayGatsby.jpg")

project1RoleId3 = createProjectRole(projectID=project1ProjectID,
								 		    username="amybolt",
								 		    title="Female lead",
								 		    characterName="Daisy Buchanan",
								 		    characterDescription=daisyBuchananDescription,
								 		    location="UBC Campus",
								 		    status="Cast",
								 		    picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/daisyBuchanan.png")

project1RoleId4 = createProjectRole(projectID=project1ProjectID,
								 		    title="Child lead - female",
								 		    characterName="Lizzy",
								 		    characterDescription=daisyBuchananDescription,
								 		    location="UBC Campus",
								 		    compensationType="Negotiable",
								 		    compensationDescription="Will be discussed with parents/guardians",
								 		    gender="Female",
								 		    status="Open")

project1RoleId5 = createProjectRole(projectID=project1ProjectID,
								 		     title="Child lead - male",
								 		     characterName="Kevin",
								 		     gender="Male",
								 		     location="UBC Campus",
								 		     characterDescription="13-15 stupid looking boy, Dammit Kevin.",
								 		     status="Open")
								 		    
project1RoleId6 = createProjectRole(projectID=project1ProjectID,
									poster="mattgray",
								 	title="Looking for young 20-something male to play a random guy",
								 	characterName="Clark",
								 	location="UBC Campus",
								 	characterDescription="Looks like he comes from a wealthy family",
								 	status="Open")
project1RoleId7 = createProjectRole(projectID=project1ProjectID,
								 	poster="mattgray",
								 	title="Looking for young 20-something female to play a random guy's gf",
								 	characterName="Mona Lisa Saperstein",
								 	characterDescription = "She is the worst. It is unbelievable how bad she is. She is the brother of jean rakphio saperstein, so actress must look related.",
								 	location="UBC Campus",
								 	status="Open",
								 	picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/randomChickDrawing.jpg")

project2JobId1 = createProjectJob(projectID=project7ProjectPost.projectID,
								 		    username="johnstongray",
								 		    title="Creator",
								 		    description="I wrote the whole thing",
								 		    profession="Director",
								 		    status="Filled")

project2RoleId1 = createProjectRole(projectID=project7ProjectPost.projectID,
								 	username="johnstongray",
								 	title="blah",
								 	characterName="James",
								 	characterDescription="Own the room",
								 	status="Cast")

# Open table read event
eightPM = datetime.time(20, 0, 0, 0)
tenPM = datetime.time(22, 0, 0, 0)
project1EventPostID = createProjectEvent(projectID=project1ProjectID,
								 poster="mattgray",
								 host="Matt Gray",
								 title="Open casting call",
								 description="Casting for all roles",
								 location="Hyatt Vancouver",
								 startDate=datetime.datetime(2017, 06, 02),
								 endDate=datetime.datetime(2017, 06, 02),
								 startTime=eightPM,
								 endTime=tenPM,
								 admissionInfo="Open to public",
								 picURL="/Users/MattGray/Projects/Agency/Agency/scripts/media/castingCall.jpeg")
project1EventPostID2 = createProjectEvent(projectID=project1ProjectID,
								 poster="mattgray",
								 host="ZOOM Film Festival",
								 title="Screening",
								 description="Ongoing showcase of final cut at the Zoom film festival",
								 location="Oprheum Theatre",
								 startDate=datetime.datetime(2017, 8, 4),
								 endDate=datetime.datetime(2017, 9, 10),
								 startTime=eightPM,
								 endTime=tenPM,
								 admissionInfo="Entrance is by donation")

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
