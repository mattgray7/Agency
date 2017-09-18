import forms
import models

import post
import home
import profile
import browse
import account

import post_casting as castingPost
import post_event as eventPost
import post_project as projectPost
import post_work as workPost
import post_collaboration as collaborationPost

NO_PICTURE_PATH = "/media/default/noPicture.jpg"
NO_PROFILE_PICTURE_PATH = "/media/default/noProfilePicture.jpg"
LOADING_GIF = "/media/default/loading.gif"
PLUS_SIGN_PATH = "/media/default/plus.png"

# Source page enums:
HOME = "HOME"
LOGIN = "LOGIN"
LOGOUT = "LOGOUT"
CANCEL = "CANCEL"
PROFILE = "PROFILE"

# Post types
EVENT_POST = "EVENT_POST"
PROJECT_POST = "PROJECT_POST"
COLLABORATION_POST = "COLLABORATION_POST"
WORK_POST = "WORK_POST"
CASTING_POST = "CASTING_POST"

CREATE_POST = "CREATE_POST"
CREATE_POST_CHOICE = "CREATE_POST_CHOICE"
VIEW_POST = "VIEW_POST"
EDIT_POST = "EDIT_POST"

CREATE_EVENT_POST = "CREATE_EVENT_POST"
CREATE_PROJECT_POST = "CREATE_PROJECT_POST"
CREATE_COLLABORATION_POST = "CREATE_COLLABORATION_POST"
CREATE_WORK_POST = "CREATE_WORK_POST"
CREATE_CASTING_POST = "CREATE_CASTING_POST"

"""BROWSE_CHOICE = "BROWSE_CHOICE"
BROWSE_POSTS = "BROWSE_POSTS"
BROWSE_EVENTS = "BROWSE_EVENTS"
BROWSE_PROJECTS = "BROWSE_PROJECTS"
BROWSE_USERS = "BROWSE_USERS"""
BROWSE = "BROWSE"

RANDOM_ID_LENGTH = 6

DEFAULT = "DEFAULT"
MANUAL_FORM_CLASS = "MANUAL_FORM_CLASS"
DJANGO_FORM_CLASS = "DJANGO_FORM_CLASS"

CREATE_BASIC_ACCOUNT = "CREATE_BASIC_ACCOUNT"
CREATE_BASIC_ACCOUNT_FINISH = "CREATE_BASIC_ACCOUNT_FINISH"
SETUP_ACCOUNT_FINISH = "SETUP_ACCOUNT_FINISH"

EDIT_INTERESTS = "EDIT_INTERESTS"
EDIT_PROFILE_PICTURE = "EDIT_PROFILE_PICTURE"
EDIT_BACKGROUND = "EDIT_BACKGROUND"
EDIT_ACTOR_DESCRIPTION = "EDIT_ACTOR_DESCRIPTION"

PROFESSIONS = {"acting": ["Actor", "Dancer", "Extra", "Stand-in", "Model", "Voice Actor"],
			   "creative": ["Art Director", "Director", "Director of Photography", "Graphic Designer",
			   				"Film Festival Director", "Musician", "Screenwriter", "Songwriter"],
			   "onSetProduction": ["Assistant Director","Assistant Camera Operator",
			   					   "Boom Operator", "Camera Operator", "Caterer", "Cinematographer",
			   					   "Electrician", "Grip", "Hair Stylist", "Key Grip", "Lighting Technician",
			   					   "Location Manager", "Makeup Artist", "Photographer", "Production Assistant",
			   					   "Prop Master", "Script Coordinator", "Set Coordinator", "Set Decorator",
			   					   "Set Designer", "SFX Technician", "SFX Supervisor", "Stunt Coordinator",
			   					   "Stunt Artist", "Wardrobe Supervisor"],
			   "offSetProduction": ["Acting Coach", "Art Director", "Producer", "Production Coordinator",
			   						"Production Designer", "Production Manager", "Voice Artist"],
			   "preProduction": ["Casting Director", "Choreographer", "Costume Designer", "Concept Artist",
			   					 "Producer", "Screenwriter", "Storyboard Artist"],
			   "postProduction": ["CG Animator", "Digital Compositor", "Editor", "Marketing", "Music Composer",
			   					  "Music Supervisor", "Music Editor", "Producer", "Sound Editor", "Sound Engineer",
			   					  "VFX Artist", "VFX Supervisor"]}

PROFESSION_LIST = []
for category in PROFESSIONS:
	for profession in PROFESSIONS[category]:
		PROFESSION_LIST.append(profession)
PROFESSION_LIST = sorted(list(set(PROFESSION_LIST)))


HIRE_TYPES = ["hireProject", "hirePermanent", "casting", "collaborating"]
COLLABORATOR_OPTIONS = ["Director", "Director of photography", "Musical artist", "Screenwriter", "Story writer", "Other"]


GENDER_OPTIONS = ["-", "Male", "Female", "Non-binary", "Other", "Prefer not to specify"]	# used in other places than actor attribute
CHARACTER_TYPE_OPTIONS = ["Actor", "Extra", "Model", "Chorus member", "Dancer", "Other"]
AGE_RANGE_OPTIONS = ["-", "0 - 6", "6 - 12", "12 - 16", "16 - 20", "20 - 25", "25 - 40", "40 - 55", "55 - 70", "70+"]
HAIR_COLOR_OPTIONS = ["-", "Black", "Blonde", "Brown", "Grey", "Red", "White", "Other"]
EYE_COLOR_OPTIONS = ["-", "Blue", "Brown", "Green", "Grey", "Other"]
ETHNICITY_OPTIONS = ["-", "Caucasian", "Latino", "African", "East Asian", "Middle Eastern", "Indian"]
BUILD_OPTIONS = ["-", "Slim", "Medium", "Muscular", "Large"]

ACTOR_ATTRIBUTE_DICT = [{"name": "hairColor",
						 "options": HAIR_COLOR_OPTIONS},
						{"name": "eyeColor",
						 "options": EYE_COLOR_OPTIONS},
						{"name": "ethnicity",
						 "options": ETHNICITY_OPTIONS},
						{"name": "ageRange",
						 "options": AGE_RANGE_OPTIONS},
						{"name": "gender",
						 "options": GENDER_OPTIONS},
						{"name": "height"},
						{"name": "build",
						 "options": BUILD_OPTIONS},
						{"name": "characterType",
						 "options": CHARACTER_TYPE_OPTIONS}
						 ]

ACTOR_DESCRIPTION_PAGE_TYPES = {"castingPost": CASTING_POST,
								"profile": PROFILE}

PROJECT_TYPE_LIST = ["Film - Feature", "Film - Short", "Television", "Competition", "Commercial", "Promotional", "Student", "Web Series", "Other"]
PROJECT_STATUS_LIST = ["Pre-production", "In production", "Post production", "Screening", "Completed"]
CASTING_STATUS_LIST = ["Opening soon", "Open", "Cast"]
WORK_STATUS_LIST = ["Opening soon", "Open", "Filled"]
EVENT_STATUS_LIST = ["Today", "Upcoming", "Past", "Announced", "Cancelled"]
PROFILE_STATUS_LIST = ["Currently available", "Currently unavailable"]
COMPENSATION_TYPES = ["Paid", "Negotiable", "Unpaid"]

PARTICIPATION_LABEL_SELECT_FIELDS = {"roles": ["Interested", "Awaiting Response", "Offer Pending", "Cast"],
									 "jobs": ["Interested", "Awaiting Response", "Offer Pending", "Hired"],
									 "events": ["Invited", "Attending", "Not Attending"],
									 "project": ["Creator", "Director", "Producer", "Writer", "Other"]}

URL_MAP = {HOME: "/",
		   LOGIN:"/login/",
		   PROFILE:"/user/{0}/",

		   # Account creation
		   CREATE_BASIC_ACCOUNT: "/account/create/basic/",
		   CREATE_BASIC_ACCOUNT_FINISH: "/account/create/finish/",
		   SETUP_ACCOUNT_FINISH: "/account/create/finish/",
		   EDIT_INTERESTS: "/account/edit/interests/",
		   EDIT_PROFILE_PICTURE: "/account/edit/picture/",
		   EDIT_BACKGROUND: "/account/edit/background/",
		   EDIT_ACTOR_DESCRIPTION: "/account/edit/description/",

		   # Post creation
		   CREATE_POST: "/post/",
		   CREATE_POST_CHOICE: "/post/create/",
		   EDIT_POST: "/post/edit/{0}/",
		   VIEW_POST: "/post/view/{0}/",
		   CREATE_EVENT_POST: "/post/create/event/",
		   CREATE_PROJECT_POST: "/post/create/project/",
		   CREATE_COLLABORATION_POST: "/post/create/collaboration/",
		   CREATE_WORK_POST: "/post/create/work/",
		   CREATE_CASTING_POST: "/post/create/casting/",
		   
		   # Browse
		   BROWSE: "/browse/"
		   }



DEFAULT_PAGE_MAP = {HOME: HOME,
					PROFILE: PROFILE,
					LOGIN: HOME,
					LOGOUT: HOME,

					# Account creations
					CREATE_BASIC_ACCOUNT: CREATE_BASIC_ACCOUNT_FINISH,
					CREATE_BASIC_ACCOUNT_FINISH: EDIT_INTERESTS,
					EDIT_INTERESTS: EDIT_PROFILE_PICTURE,
					EDIT_PROFILE_PICTURE: EDIT_BACKGROUND,
					EDIT_BACKGROUND: HOME,
					EDIT_ACTOR_DESCRIPTION: HOME,
					SETUP_ACCOUNT_FINISH: HOME,

					# Post creation
					CREATE_POST: CREATE_POST,
					CREATE_EVENT_POST: VIEW_POST,
					CREATE_POST_CHOICE: CREATE_PROJECT_POST,
					EDIT_POST: VIEW_POST,
					VIEW_POST: VIEW_POST,
					CREATE_EVENT_POST: VIEW_POST,
					CREATE_PROJECT_POST: VIEW_POST,
					CREATE_WORK_POST: VIEW_POST,
					CREATE_COLLABORATION_POST: VIEW_POST,
					CREATE_CASTING_POST: VIEW_POST,

					# Browse
					BROWSE: BROWSE
					}



FORM_MAP = {HOME: forms.BaseForm,
			PROFILE: forms.BaseForm,
			LOGIN: forms.LoginForm,

			# Account creation
			CREATE_BASIC_ACCOUNT: forms.CreateAccountForm,
			EDIT_INTERESTS: forms.EditInterestsForm,
			EDIT_PROFILE_PICTURE: forms.EditPictureForm,
			EDIT_BACKGROUND: forms.EditBackgroundForm,
			EDIT_ACTOR_DESCRIPTION: None, #manual

			# Post creation
			CREATE_EVENT_POST: forms.CreateEventPostForm,
			CREATE_POST_CHOICE: None,
			CREATE_PROJECT_POST: forms.CreateProjectPostForm,
			CREATE_COLLABORATION_POST: forms.CreateCollaborationPostForm,
			CREATE_WORK_POST: forms.CreateWorkPostForm,
			CREATE_CASTING_POST: forms.CreateCastingPostForm,
			EDIT_POST: None,
			VIEW_POST: None
			}

VIEW_CLASS_MAP = {HOME: home.HomeView,
				  LOGIN: account.LoginView,
				  LOGOUT: account.LogoutView,
			   	  PROFILE: profile.ProfileView,
                  BROWSE: browse.BrowseView,

			   	  # Create posts
			   	  CREATE_POST: post.CreatePostTypesView,	# event, project, work, collab, casting
			   	  CREATE_POST_CHOICE: post.CreatePostChoiceView,		# just btw work, collab, and casting
			   	  CREATE_EVENT_POST: eventPost.CreateEventPostView,
			   	  CREATE_PROJECT_POST: projectPost.CreateProjectPostView,
			   	  CREATE_WORK_POST: workPost.CreateWorkPostView,
			   	  CREATE_CASTING_POST: castingPost.CreateCastingPostView,
			   	  CREATE_COLLABORATION_POST: collaborationPost.CreateCollaborationPostView,

			   	  # Account creation:
			   	  CREATE_BASIC_ACCOUNT: account.CreateAccountView,
			   	  CREATE_BASIC_ACCOUNT_FINISH: account.CreateAccountFinishView,
			   	  EDIT_INTERESTS: account.EditInterestsView,
			   	  EDIT_PROFILE_PICTURE: account.EditPictureView,
			   	  EDIT_BACKGROUND: account.EditBackgroundView,
			   	  EDIT_ACTOR_DESCRIPTION: account.EditActorDescriptionView
			   	  }

HTML_MAP = {HOME: 'AgencyApp/home.html',
			LOGIN: 'AgencyApp/account/login.html',
			PROFILE: 'AgencyApp/profile.html',

			# Account creation
			CREATE_BASIC_ACCOUNT: 'AgencyApp/account/create.html',
			CREATE_BASIC_ACCOUNT_FINISH: 'AgencyApp/account/finish.html',
			SETUP_ACCOUNT_FINISH: 'AgencyApp/account/finish.html',
			#EDIT_INTERESTS: 'AgencyApp/account/interests.html',
			#EDIT_BACKGROUND: 'AgencyApp/account/background.html',
			#EDIT_PROFILE_PICTURE: 'AgencyApp/account/picture.html',
			EDIT_INTERESTS: 'AgencyApp/account/edit.html',
			EDIT_PROFILE_PICTURE: 'AgencyApp/account/edit.html',
			EDIT_BACKGROUND: 'AgencyApp/account/edit.html',
			EDIT_ACTOR_DESCRIPTION: 'AgencyApp/account/actorDescription.html',

			# Post creation
			CREATE_POST: 'AgencyApp/post/post.html',
			CREATE_POST_CHOICE: 'AgencyApp/post/postChoice.html',
			VIEW_POST: 'AgencyApp/post/viewPost.html',
			EDIT_POST: None,
			CREATE_EVENT_POST: 'AgencyApp/post/createPost.html',
			CREATE_PROJECT_POST: 'AgencyApp/post/createProjectPost.html',
			CREATE_COLLABORATION_POST: 'AgencyApp/post/createPost.html',
			CREATE_WORK_POST: 'AgencyApp/post/createPost.html',
			CREATE_CASTING_POST: 'AgencyApp/post/createPost.html',

			# Browse
			BROWSE: 'AgencyApp/browse.html'
			}


MEDIA_FILE_NAME_MAP = {EDIT_PROFILE_PICTURE: "profile.jpg",
					   EVENT_POST: "event_{0}.jpg",
					   COLLABORATION_POST: "collaboration_{0}.jpg",
					   WORK_POST: "work_{0}.jpg",
					   PROJECT_POST: "project_{0}.jpg",
					   CASTING_POST: "casting_{0}.jpg"
					   }

POST_DATABASE_MAP = {EVENT_POST: models.EventPost,
					 PROJECT_POST: models.ProjectPost,
					 COLLABORATION_POST: models.CollaborationPost,
					 WORK_POST: models.WorkPost,
					 CASTING_POST: models.CastingPost}

CREATE_POST_PAGE_MAP = {EVENT_POST: CREATE_EVENT_POST,
						PROJECT_POST: CREATE_PROJECT_POST,
						COLLABORATION_POST: CREATE_COLLABORATION_POST,
						WORK_POST: CREATE_WORK_POST,
						CASTING_POST: CREATE_CASTING_POST}
"""
BROWSE_POST_PAGE_MAP = {EVENT_POST: BROWSE_EVENTS,
                        PROFILE: BROWSE_USERS,
                        PROJECT_POST: BROWSE_PROJECTS,
                        COLLABORATION_POST: BROWSE_POSTS,
                        WORK_POST: BROWSE_POSTS,
                        CASTING_POST: BROWSE_POSTS}"""

