import forms

# Source page enums:
HOME = "HOME"
LOGIN = "LOGIN"
PROFILE = "PROFILE"
CREATE_POST = "CREATE_POST"
CREATE_EVENT = "CREATE_EVENT"

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
		   CREATE_BASIC_ACCOUNT_FINISH: "/account/create/finish/",
		   SETUP_ACCOUNT_FINISH: "/account/create/finish/",
		   EDIT_INTERESTS: "/account/edit/interests/",
		   EDIT_PROFESSIONS: "/account/edit/professions/",
		   EDIT_PROFILE_PICTURE: "/account/edit/picture/",
		   EDIT_BACKGROUND: "/account/edit/background/"
		   }

# format is {currentPage: {source1: dest1, source2:dest2, source3: {pagekey1: dest3-1, pagekey2: dest3-2}}}
PAGE_MAP = {DEFAULT: HOME,
			LOGIN: {HOME: {DEFAULT: HOME,
						   HOME: HOME,
						   CREATE_EVENT: CREATE_EVENT,
						   CREATE_POST: CREATE_POST}},
			CREATE_BASIC_ACCOUNT: {LOGIN: {DEFAULT: CREATE_BASIC_ACCOUNT_FINISH}},
			EDIT_INTERESTS: {PROFILE: {DEFAULT: PROFILE},
							 CREATE_BASIC_ACCOUNT_FINISH: {DEFAULT: EDIT_PROFESSIONS}},
			EDIT_PROFESSIONS: {PROFILE: {DEFAULT: PROFILE},
							   EDIT_INTERESTS: {DEFAULT: EDIT_PROFILE_PICTURE}},
			EDIT_PROFILE_PICTURE: {PROFILE: {DEFAULT: PROFILE},
								   EDIT_PROFESSIONS: {DEFAULT: EDIT_BACKGROUND}},
			EDIT_BACKGROUND: {PROFILE: {DEFAULT: PROFILE},
							  EDIT_PROFILE_PICTURE: {DEFAULT: SETUP_ACCOUNT_FINISH}}
			}

FORM_MAP = {LOGIN: forms.LoginForm,
			CREATE_BASIC_ACCOUNT: forms.CreateAccountForm,
			EDIT_INTERESTS: forms.EditInterestsForm,
			EDIT_PROFESSIONS: None,	#manual
			EDIT_PROFILE_PICTURE: forms.EditPictureForm,
			EDIT_BACKGROUND: forms.EditBackgroundForm
			}

HTML_MAP = {EDIT_INTERESTS: 'AgencyApp/account/interests.html'}







