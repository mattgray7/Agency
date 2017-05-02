import forms

# Source page enums:
HOME = "HOME"
LOGIN = "LOGIN"
LOGOUT = "LOGOUT"
CANCEL = "CANCEL"
PROFILE = "PROFILE"
CREATE_POST = "CREATE_POST"
CREATE_EVENT = "CREATE_EVENT"
EDIT_EVENT = "EDIT_EVENT"
VIEW_EVENT = "VIEW_EVENT"

BROWSE_EVENTS = "BROWSE_EVENTS"
BROWSE_POSTS = "BROWSE_POSTS"

EVENT_ID_LENGTH = 8

DEFAULT = "DEFAULT"
MANUAL_FORM_CLASS = "MANUAL_FORM_CLASS"
DJANGO_FORM_CLASS = "DJANGO_FORM_CLASS"

TOOLBAR_LOGIN = "TOOLBAR_LOGIN"
TOOLBAR_HOME = "TOOLBAR_HOME"
TOOLBAR_LOGOUT = "TOOLBAR_LOGOUT"
TOOLBAR_PROFILE = "TOOLBAR_PROFILE"

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
		   CREATE_POST: "/create/post/choose/",
		   CREATE_EVENT: "/create/event/",
		   EDIT_EVENT: "/edit/event/{0}/",
		   VIEW_EVENT: "/view/event/{0}/",
		   CREATE_BASIC_ACCOUNT_FINISH: "/account/create/finish/",
		   SETUP_ACCOUNT_FINISH: "/account/create/finish/",
		   EDIT_INTERESTS: "/account/edit/interests/",
		   EDIT_PROFESSIONS: "/account/edit/professions/",
		   EDIT_PROFILE_PICTURE: "/account/edit/picture/",
		   EDIT_BACKGROUND: "/account/edit/background/",
		   BROWSE_EVENTS: "/browse/events/",
		   BROWSE_POSTS: "/browse/posts/"
		   }


DEFAULT_CANCEL_URL_MAP = {CREATE_EVENT: "/create/event/",
						  EDIT_EVENT: "/edit/event/{0}/",
						  EDIT_INTERESTS: "/account/edit/interests/",
						  EDIT_PROFESSIONS: "/account/edit/professions/",
						  EDIT_PROFILE_PICTURE: "/account/edit/picture/",
						  EDIT_BACKGROUND: "/account/edit/background/",
						  PROFILE: "/{0}/"
						  }

DEFAULT_PAGE_MAP = {HOME: HOME,
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
					VIEW_EVENT: VIEW_EVENT,
					CREATE_EVENT: VIEW_EVENT,
					EDIT_EVENT: VIEW_EVENT,
					BROWSE_EVENTS: VIEW_EVENT}

FORM_MAP = {LOGIN: forms.LoginForm,
			CREATE_BASIC_ACCOUNT: forms.CreateAccountForm,
			EDIT_INTERESTS: forms.EditInterestsForm,
			EDIT_PROFESSIONS: None,	#manual
			EDIT_PROFILE_PICTURE: forms.EditPictureForm,
			EDIT_BACKGROUND: forms.EditBackgroundForm,
			CREATE_EVENT: forms.CreateEventForm,
			EDIT_EVENT: forms.CreateEventForm,
			VIEW_EVENT: forms.CreateEventForm,
			}

HTML_MAP = {LOGIN: 'AgencyApp/account/login.html',
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
			BROWSE_EVENTS: 'AgencyApp/browse.html',
			BROWSE_POSTS: 'AgencyApp/browse.html'}

MEDIA_FILE_NAME_MAP = {EDIT_PROFILE_PICTURE: "profile.jpg",
					   CREATE_EVENT: "event_{0}.jpg"}







