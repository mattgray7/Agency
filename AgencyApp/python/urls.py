import views
import ajax
import constants

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.handleURL, name=constants.HOME),
    url(r'^login/$', views.handleURL, name=constants.LOGIN),
    url(r'^logout/$', views.handleURL, name=constants.LOGOUT),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.handleUsernameURL, name=constants.PROFILE),

    # Create account
    url(r'^account/create/basic/$', views.handleURL, name=constants.CREATE_BASIC_ACCOUNT),
    url(r'^account/create/finish/$', views.handleURL, name=constants.CREATE_BASIC_ACCOUNT_FINISH),
    url(r'^account/edit/picture/$', views.handleURL, name=constants.EDIT_PROFILE_PICTURE),
    url(r'^account/edit/interests/$', views.handleURL, name=constants.EDIT_INTERESTS,),
    url(r'^account/edit/background/$', views.handleURL, name=constants.EDIT_BACKGROUND),
    url(r'^account/edit/description/$', views.handleURL, name=constants.EDIT_ACTOR_DESCRIPTION),

    # Create posts
    url(r'^post/$', views.handleURL, name=constants.CREATE_POST),
    url(r'^post/create/$', views.handleURL, name=constants.CREATE_POST_CHOICE),
    url(r'^post/edit/(?P<postID>[A-Za-z0-9]+)/$', views.handleEditPostIDURL, name=constants.EDIT_POST),
    url(r'^post/view/(?P<postID>[A-Za-z0-9]+)/$', views.handleViewPostIDURL, name=constants.VIEW_POST),
    url(r'^post/create/event/$', views.handleURL, name=constants.CREATE_EVENT_POST),
    url(r'^post/create/collaboration/$', views.handleURL, name=constants.CREATE_COLLABORATION_POST),
    url(r'^post/create/work/$', views.handleURL, name=constants.CREATE_WORK_POST),
    url(r'^post/create/project/$', views.handleURL, name=constants.CREATE_PROJECT_POST),
    url(r'^post/create/casting/$', views.handleURL, name=constants.CREATE_CASTING_POST),

    # Ajax calls
    url(r'^post/view/(?P<postID>[A-Za-z0-9]+)/follow/$', ajax.followPost, name='followPost'),
    url(r'^ajax/getPostFollowingBool/$', ajax.getPostFollowingBool, name='getPostFollowingBool'),
    url(r'^ajax/getUserProjects/$', ajax.getUserProjects, name='getUserProjects'),
    url(r'^ajax/deletePostFromDB/$', ajax.deletePostFromDB, name='deletePostFromDB'),  #TODO find a way to secure this link
    url(r'^ajax/deleteProfilePicture/$', ajax.deleteProfilePicture, name='deleteProfilePicture'),  #TODO find a way to secure this link
    url(r'^ajax/deletePostPicture/$', ajax.deletePostPicture, name='deletePostPicture'),  #TODO find a way to secure this link
    url(r'^ajax/getNewPostID/$', ajax.getNewPostID, name='getNewPostID'),  #TODO find a way to secure this link
    url(r'^ajax/getPostData/$', ajax.getPostData, name='getPostData'),  #TODO find a way to secure this link
    url(r'^ajax/createNewCastingPost/$', ajax.createNewCastingPost, name='createNewCastingPost'),  #TODO find a way to secure this link
    url(r'^ajax/createNewWorkPost/$', ajax.createNewWorkPost, name='createNewWorkPost'),  #TODO find a way to secure this link
    url(r'^ajax/createNewEventPost/$', ajax.createNewEventPost, name='createNewEventPost'),  #TODO find a way to secure this link
    url(r'^ajax/editExistingPost/$', ajax.editExistingPost, name='editExistingPost'),
    url(r'^ajax/updatePostPicture/$', ajax.updatePostPicture, name='updatePostPicture'),  #TODO find a way to secure this link
    url(r'^ajax/saveTempPostPicture/$', ajax.saveTempPostPicture, name='saveTempPostPicture'),  #TODO find a way to secure this link
    url(r'^ajax/savePostParticipant/$', ajax.savePostParticipant, name='savePostParticipant'),  #TODO find a way to secure this link

    url(r'^ajax/getSearchPreviewActors/$', ajax.getSearchPreviewActors, name='getSearchPreviewActors'),  #TODO find a way to secure this link


    # Browse
    url(r'^browse/$', views.handleURL, name=constants.BROWSE_CHOICE),
    url(r'^browse/events/$', views.handleURL, name=constants.BROWSE_EVENTS),
    url(r'^browse/projects/$', views.handleURL, name=constants.BROWSE_PROJECTS),
    url(r'^browse/users/$', views.handleURL, name=constants.BROWSE_USERS),
    url(r'^browse/posts/$', views.handleURL, name=constants.BROWSE_POSTS),
]
