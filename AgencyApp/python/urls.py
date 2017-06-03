import views
import ajax
import constants

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.handleURL, name=constants.HOME),

    # Create account
    url(r'^account/create/basic/$', views.createAccount, name='createAccount'),
    url(r'^account/create/finish/$', views.createAccountFinish, name='createAccountFinish'),
    url(r'^account/edit/picture/$', views.editPicture, name='editPicture'),
    url(r'^account/edit/interests/$', views.editInterests, name='editInterests'),
    url(r'^account/edit/professions/$', views.editProfessions, name='editProfessions'),
    url(r'^account/edit/background/$', views.editBackground, name='editBackground'),
    url(r'^account/edit/description/$', views.editActorDescription, name='editActorDescription'),

    # Create posts
    url(r'^post/$', views.handleURL, name=constants.CREATE_POST),
    url(r'^post/create/$', views.handleURL, name=constants.CREATE_POST_CHOICE),
    url(r'^post/edit/(?P<postID>[A-Za-z0-9]+)/$', views.handleEditPostIDURL, name=constants.EDIT_POST),
    url(r'^post/view/(?P<postID>[A-Za-z0-9]+)/$', views.handleViewPostIDURL, name=constants.VIEW_POST),
    url(r'^post/create/event/$', views.createEventPost, name='createEvent'),
    url(r'^post/create/collaboration/$', views.createCollaborationPost, name='createCollaborationPost'),
    url(r'^post/create/work/$', views.createWorkPost, name='createWorkPost'),
    url(r'^post/create/project/$', views.createProjectPost, name='createProjectPost'),
    url(r'^post/create/casting/$', views.createCastingPost, name='createCastingPost'),

    # Ajax calls
    url(r'^post/view/(?P<postID>[A-Za-z0-9]+)/follow/$', ajax.followPost, name='followPost'),
    url(r'^ajax/getPostFollowingBool/$', ajax.getPostFollowingBool, name='getPostFollowingBool'),
    url(r'^ajax/getUserProjects/$', ajax.getUserProjects, name='getUserProjects'),
    url(r'^ajax/deletePostFromDB/$', ajax.deletePostFromDB, name='deletePostFromDB'),  #TODO find a way to secure this link


    # Browse
    url(r'^browse/$', views.handleURL, name=constants.BROWSE_CHOICE),
    url(r'^browse/events/$', views.handleURL, name=constants.BROWSE_EVENTS),
    url(r'^browse/projects/$', views.handleURL, name=constants.BROWSE_PROJECTS),
    url(r'^browse/users/$', views.handleURL, name=constants.BROWSE_USERS),
    url(r'^browse/posts/$', views.handleURL, name=constants.BROWSE_POSTS),

    # Other
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    #url(r'^ajax/$', ajax.call, name='ajax'),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.handleUsernameURL, name=constants.PROFILE),
]
