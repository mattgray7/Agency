import forms
import models

# Source page enums:
HOME = "HOME"
LOGIN = "LOGIN"
LOGOUT = "LOGOUT"
CANCEL = "CANCEL"
PROFILE = "PROFILE"

CREATE_EVENT = "CREATE_EVENT"
EDIT_EVENT = "EDIT_EVENT"
VIEW_EVENT = "VIEW_EVENT"

CREATE_POST_CHOICE = "CREATE_POST_CHOICE"
VIEW_POST = "VIEW_POST"
EDIT_POST = "EDIT_POST"

CREATE_PROJECT_POST = "CREATE_PROJECT"
CREATE_COLLABORATION_POST = "CREATE_COLLABORATION_POST"
CREATE_WORK_POST = "CREATE_WORK_POST"

BROWSE_EVENTS = "BROWSE_EVENTS"
BROWSE_POSTS = "BROWSE_POSTS"

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
		   PROFILE:"/{0}/",
		   CREATE_BASIC_ACCOUNT: "/account/create/basic/",
		   CREATE_EVENT: "/create/event/",
		   EDIT_EVENT: "/edit/event/{0}/",
		   VIEW_EVENT: "/view/event/{0}/",
		   CREATE_POST_CHOICE: "/create/post/",
		   EDIT_POST: "/edit/post/{0}/",
		   VIEW_POST: "/view/post/{0}/",
		   CREATE_PROJECT_POST: "/create/project/",
		   CREATE_COLLABORATION_POST: "/create/post/collaboration/",
		   CREATE_WORK_POST: "/create/post/work/",
		   CREATE_BASIC_ACCOUNT_FINISH: "/account/create/finish/",
		   SETUP_ACCOUNT_FINISH: "/account/create/finish/",
		   EDIT_INTERESTS: "/account/edit/interests/",
		   EDIT_PROFESSIONS: "/account/edit/professions/",
		   EDIT_PROFILE_PICTURE: "/account/edit/picture/",
		   EDIT_BACKGROUND: "/account/edit/background/",
		   BROWSE_EVENTS: "/browse/events/",
		   BROWSE_POSTS: "/browse/posts/"
		   }

DEFAULT_PAGE_MAP = {HOME: HOME,
					PROFILE: PROFILE,
					LOGIN: HOME,
					LOGOUT: HOME,
					CREATE_BASIC_ACCOUNT: CREATE_BASIC_ACCOUNT_FINISH,
					CREATE_BASIC_ACCOUNT_FINISH: EDIT_INTERESTS,
					EDIT_INTERESTS: EDIT_PROFESSIONS,
					EDIT_PROFESSIONS: EDIT_PROFILE_PICTURE,
					EDIT_PROFILE_PICTURE: EDIT_BACKGROUND,
					EDIT_BACKGROUND: SETUP_ACCOUNT_FINISH,
					SETUP_ACCOUNT_FINISH: HOME,
					PROFILE: PROFILE,
					CREATE_EVENT: VIEW_EVENT,
					VIEW_EVENT: VIEW_EVENT,
					EDIT_EVENT: VIEW_EVENT,
					BROWSE_EVENTS: VIEW_EVENT,
					CREATE_POST_CHOICE: CREATE_PROJECT_POST,
					EDIT_POST: VIEW_POST,
					CREATE_PROJECT_POST: CREATE_WORK_POST,
					CREATE_WORK_POST: VIEW_POST,
					CREATE_COLLABORATION_POST: VIEW_POST,
					VIEW_POST: VIEW_POST
					}

FORM_MAP = {HOME: forms.BaseForm,
			PROFILE: forms.BaseForm,
			LOGIN: forms.LoginForm,
			CREATE_BASIC_ACCOUNT: forms.CreateAccountForm,
			EDIT_INTERESTS: forms.EditInterestsForm,
			EDIT_PROFESSIONS: None,	#manual
			EDIT_PROFILE_PICTURE: forms.EditPictureForm,
			EDIT_BACKGROUND: forms.EditBackgroundForm,
			CREATE_EVENT: forms.CreateEventForm,
			EDIT_EVENT: forms.CreateEventForm,
			VIEW_EVENT: forms.CreateEventForm,
			CREATE_POST_CHOICE: None,
			CREATE_PROJECT_POST: forms.CreateProjectPostForm,
			CREATE_COLLABORATION_POST: forms.CreateCollaborationPostForm,
			CREATE_WORK_POST: forms.CreateWorkPostForm,
			EDIT_POST: None,
			VIEW_POST: None
			}

HTML_MAP = {HOME: 'AgencyApp/home.html',
			LOGIN: 'AgencyApp/account/login.html',
			PROFILE: 'AgencyApp/profile.html',
			CREATE_BASIC_ACCOUNT: 'AgencyApp/account/create.html',
			CREATE_BASIC_ACCOUNT_FINISH: 'AgencyApp/account/finish.html',
			SETUP_ACCOUNT_FINISH: 'AgencyApp/account/finish.html',
			EDIT_INTERESTS: 'AgencyApp/account/interests.html',
			EDIT_PROFESSIONS: 'AgencyApp/account/professions.html',
			EDIT_BACKGROUND: 'AgencyApp/account/background.html',
			EDIT_PROFILE_PICTURE: 'AgencyApp/account/picture.html',
			CREATE_EVENT: 'AgencyApp/event/create.html',
			EDIT_EVENT: 'AgencyApp/event/create.html',
			VIEW_EVENT: 'AgencyApp/event/view.html',
			CREATE_POST_CHOICE: 'AgencyApp/post/createPostChoice.html',
			VIEW_POST: 'AgencyApp/post/viewPost.html',
			EDIT_POST: None,
			CREATE_PROJECT_POST: 'AgencyApp/post/project.html',
			CREATE_COLLABORATION_POST: 'AgencyApp/post/createCollaborationPost.html',
			CREATE_WORK_POST: 'AgencyApp/post/createWorkPost.html',
			BROWSE_EVENTS: 'AgencyApp/browse.html',
			BROWSE_POSTS: 'AgencyApp/browse.html'
			}


MEDIA_FILE_NAME_MAP = {EDIT_PROFILE_PICTURE: "profile.jpg",
					   CREATE_EVENT: "event_{0}.jpg",
					   CREATE_COLLABORATION_POST: "post_{0}.jpg",
					   CREATE_WORK_POST: "post_{0}.jpg",
					   CREATE_PROJECT_POST: "post_{0}.jpg"
					   }







