import views
import ajax

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
    url(r'^post/$', views.createPost, name='createPost'),
    url(r'^post/create/$', views.createPostChoice, name='createPostChoice'),
    url(r'^post/edit/(?P<postID>[A-Za-z0-9]+)/$', views.editPost, name='editPost'),
    url(r'^post/view/(?P<postID>[A-Za-z0-9]+)/$', views.viewPost, name='viewPost'),
    url(r'^post/create/event/$', views.createEventPost, name='createEvent'),
    url(r'^post/create/collaboration/$', views.createCollaborationPost, name='createCollaborationPost'),
    url(r'^post/create/work/$', views.createWorkPost, name='createWorkPost'),
    url(r'^post/create/project/$', views.createProjectPost, name='createProjectPost'),
    url(r'^post/create/casting/$', views.createCastingPost, name='createCastingPost'),

    # Ajax calls
    url(r'^post/view/(?P<postID>[A-Za-z0-9]+)/follow/$', ajax.followPost, name='followPost'),
    url(r'^ajax/getPostFollowingBool/$', ajax.getPostFollowingBool, name='getPostFollowingBool'),

    # Browse
    url(r'^browse/$', views.browseChoice, name='browseChoice'),
    url(r'^browse/events/$', views.browseEvents, name='browseEvents'),
    url(r'^browse/projects/$', views.browseProjects, name='browseProjects'),
    url(r'^browse/users/$', views.browseUsers, name='browseUsers'),
    url(r'^browse/posts/$', views.browsePosts, name='browsePosts'),

    # Other
    #url(r'^browse/events/$', views.browseEvents, name='browseEvents'),
    #url(r'^browse/projects/$', views.browseProjects, name='browseProjects'),
    #url(r'^browse/posts/collaboration/$', views.browseCollaborationPosts, name='browseCollaborationPosts'),
    #url(r'^browse/posts/work/$', views.browseWorkPosts, name='browseWorkPosts'),
    #url(r'^browse/posts/$', views.browsePosts, name='browsePosts'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    #url(r'^ajax/$', ajax.call, name='ajax'),
    url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.displayProfile, name='displayProfile'),
]
