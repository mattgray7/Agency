import ajax
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.displayHome, name='displayHome'),

    # Create account
    url(r'^account/create/basic/$', views.createAccount, name='createAccount'),
    url(r'^account/create/finish/$', views.createAccountFinish, name='createAccountFinish'),
    url(r'^account/edit/picture/$', views.editPicture, name='editPicture'),
    url(r'^account/edit/interests/$', views.editInterests, name='editInterests'),
    url(r'^account/edit/professions/$', views.editProfessions, name='editProfessions'),
    url(r'^account/edit/background/$', views.editBackground, name='editBackground'),

    # Create posts
    url(r'^create/event/$', views.createEvent, name='createEvent'),
    url(r'^view/event/(?P<eventID>[A-Za-z0-9]+)/$', views.viewEvent, name='viewEvent'),
    url(r'^edit/event/(?P<eventID>[A-Za-z0-9]+)/$', views.editEvent, name='editEvent'),

    # Create post
    url(r'^create/post/$', views.createPostChoice, name='createPostChoice'),
    url(r'^edit/post/(?P<postID>[A-Za-z0-9]+)/$', views.editPost, name='editPost'),
    url(r'^view/post/(?P<postID>[A-Za-z0-9]+)/$', views.viewPost, name='viewPost'),
    url(r'^create/post/collaboration/$', views.createCollaborationPost, name='createCollaborationPost'),
    url(r'^create/post/work/$', views.createWorkPost, name='createWorkPost'),
    url(r'^create/post/project/$', views.createProjectPost, name='createProjectPost'),


    # Other
    url(r'^browse/events/$', views.browseEvents, name='browseEvents'),
    url(r'^browse/projects/$', views.browseProjects, name='browseProjects'),
    url(r'^browse/posts/collaboration/$', views.browseCollaborationPosts, name='browseCollaborationPosts'),
    url(r'^browse/posts/work/$', views.browseWorkPosts, name='browseWorkPosts'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ajax/$', ajax.call, name='ajax'),
    url(r'^(?P<username>[A-Za-z0-9]+)/$', views.displayProfile, name='displayProfile'),
    url(r'^jobs/$', views.jobs, name='jobs'),
]
