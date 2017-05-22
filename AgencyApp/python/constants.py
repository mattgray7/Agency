import forms
import models

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

BROWSE = "BROWSE"
BROWSE_POSTS = "BROWSE_POSTS"
BROWSE_EVENTS = "BROWSE_EVENTS"
BROWSE_PROJECTS = "BROWSE_PROJECTS"
BROWSE_COLLABORATION_POSTS = "BROWSE_COLLABORATION_POSTS"
BROWSE_WORK_POSTS = "BROWSE_WORK_POSTS"
BROWSE_CASTING_POSTS = "BROWSE_CASTING_POSTS"

RANDOM_ID_LENGTH = 6

DEFAULT = "DEFAULT"
MANUAL_FORM_CLASS = "MANUAL_FORM_CLASS"
DJANGO_FORM_CLASS = "DJANGO_FORM_CLASS"

CREATE_BASIC_ACCOUNT = "CREATE_BASIC_ACCOUNT"
CREATE_BASIC_ACCOUNT_FINISH = "CREATE_BASIC_ACCOUNT_FINISH"
SETUP_ACCOUNT_FINISH = "SETUP_ACCOUNT_FINISH"

EDIT_INTERESTS = "EDIT_INTERESTS"
EDIT_PROFILE_PICTURE = "EDIT_PROFILE_PICTURE"
EDIT_PROFESSIONS = "EDIT_PROFESSIONS"
EDIT_BACKGROUND = "EDIT_BACKGROUND"

PROFESSIONS = ["Actor", "Acting Coach", "Art Director", "Assistant Director", "Assistant Camera Operator",
			   "Boom Operator", "Camera Operator", "Casting Director", "Choreographer", "Cinematographer",
			   "CG Animator", "Compositor", "Costume Designer", "Concept Artist", "Dancer", "Director",
			   "Editor", "Film Festival Director", "Film Festival Volunteer", "Graphic Designer", "Grip",
			   "Hair Stylist", "Key Grip", "Lighting Technician", "Location Manager", "Makeup Artist",
			   "Marketing", "Music Composer", "Music Supervisor", "Music Editor", "Musician", "Photographer",
			   "Producer", "Production Assistant", "Production Caterer", "Production Coordinator",
			   "Production Designer", "Production Manager", "Prop Master", "Screenwriter",
			   "Script Coordinator/Supervisor", "Set Coordinator", "Set Decorator", "Set Design",
			   "SFX Technician", "SFX Supervisor", "Songwriter", "Sound Editor", "Sound Engineer",
			   "Storyboard Artist", "Stunt Coordinator", "Stunt Artist", "Talent Management", "VFX Arist",
			   "VFX Supervisor", "Voice Artist", "Wardrobe Supervisor"]



URL_MAP = {HOME: "/",
		   LOGIN:"/login/",
		   PROFILE:"/user/{0}/",

		   # Account creation
		   CREATE_BASIC_ACCOUNT: "/account/create/basic/",
		   CREATE_BASIC_ACCOUNT_FINISH: "/account/create/finish/",
		   SETUP_ACCOUNT_FINISH: "/account/create/finish/",
		   EDIT_INTERESTS: "/account/edit/interests/",
		   EDIT_PROFESSIONS: "/account/edit/professions/",
		   EDIT_PROFILE_PICTURE: "/account/edit/picture/",
		   EDIT_BACKGROUND: "/account/edit/background/",
		   #CREATE_EVENT: "/create/event/",
		   #EDIT_EVENT: "/edit/event/{0}/",
		   #VIEW_EVENT: "/view/event/{0}/",

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
		   BROWSE_EVENTS: "/browse/events/",
		   BROWSE_PROJECTS: "/browse/projects/",
		   BROWSE_COLLABORATION_POSTS: "/browse/posts/collaboration/",
		   BROWSE_WORK_POSTS: "/browse/posts/work/",
		   BROWSE_CASTING_POSTS: "/browse/posts/casting/",
		   BROWSE_POSTS: "/browse/posts/",
		   BROWSE: "/browse/"
		   }



DEFAULT_PAGE_MAP = {HOME: HOME,
					PROFILE: PROFILE,
					LOGIN: HOME,
					LOGOUT: HOME,

					# Account creations
					CREATE_BASIC_ACCOUNT: CREATE_BASIC_ACCOUNT_FINISH,
					CREATE_BASIC_ACCOUNT_FINISH: EDIT_INTERESTS,
					EDIT_INTERESTS: EDIT_PROFESSIONS,
					EDIT_PROFESSIONS: EDIT_PROFILE_PICTURE,
					EDIT_PROFILE_PICTURE: EDIT_BACKGROUND,
					EDIT_BACKGROUND: SETUP_ACCOUNT_FINISH,
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
					BROWSE: BROWSE,
					BROWSE_EVENTS: VIEW_POST,
					BROWSE_PROJECTS: VIEW_POST,
					BROWSE_COLLABORATION_POSTS: VIEW_POST,
					BROWSE_WORK_POSTS: VIEW_POST,
					BROWSE_CASTING_POSTS: VIEW_POST,
					BROWSE_POSTS: VIEW_POST
					}



FORM_MAP = {HOME: forms.BaseForm,
			PROFILE: forms.BaseForm,
			LOGIN: forms.LoginForm,

			# Account creation
			CREATE_BASIC_ACCOUNT: forms.CreateAccountForm,
			EDIT_INTERESTS: forms.EditInterestsForm,
			EDIT_PROFESSIONS: None,	#manual
			EDIT_PROFILE_PICTURE: forms.EditPictureForm,
			EDIT_BACKGROUND: forms.EditBackgroundForm,

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

HTML_MAP = {HOME: 'AgencyApp/home.html',
			LOGIN: 'AgencyApp/account/login.html',
			PROFILE: 'AgencyApp/profile.html',

			# Account creation
			CREATE_BASIC_ACCOUNT: 'AgencyApp/account/create.html',
			CREATE_BASIC_ACCOUNT_FINISH: 'AgencyApp/account/finish.html',
			SETUP_ACCOUNT_FINISH: 'AgencyApp/account/finish.html',
			EDIT_INTERESTS: 'AgencyApp/account/interests.html',
			EDIT_PROFESSIONS: 'AgencyApp/account/professions.html',
			EDIT_BACKGROUND: 'AgencyApp/account/background.html',
			EDIT_PROFILE_PICTURE: 'AgencyApp/account/picture.html',

			# Post creation
			CREATE_POST: 'AgencyApp/post/post.html',
			CREATE_POST_CHOICE: 'AgencyApp/post/postChoice.html',
			VIEW_POST: 'AgencyApp/post/viewPost.html',
			EDIT_POST: None,
			CREATE_EVENT_POST: 'AgencyApp/post/createPost.html',
			CREATE_PROJECT_POST: 'AgencyApp/post/createPost.html',
			CREATE_COLLABORATION_POST: 'AgencyApp/post/createPost.html',
			CREATE_WORK_POST: 'AgencyApp/post/createPost.html',
			CREATE_CASTING_POST: 'AgencyApp/post/createPost.html',

			# Browse
			BROWSE_EVENTS: 'AgencyApp/browse.html',
			BROWSE_PROJECTS: 'AgencyApp/browse.html',
			BROWSE_COLLABORATION_POSTS: 'AgencyApp/browse.html',
			BROWSE_WORK_POSTS: 'AgencyApp/browse.html',
			BROWSE_POSTS: 'AgencyApp/browse.html',
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




