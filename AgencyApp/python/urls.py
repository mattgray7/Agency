import ajax
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.displayHome, name='displayHome'),

    # Create account
    url(r'^account/create/basic/$', views.createAccount, name='createAccount'),
    url(r'^account/edit/picture/$', views.editPicture, name='editPicture'),
    url(r'^account/edit/interests/$', views.editInterests, name='editInterests'),
    url(r'^account/edit/professions/$', views.editProfessions, name='editProfessions'),
    #url(r'^create/professions/$', views.create_selectProfessions, name='create_selectProfessions'),
    #url(r'^create/background/$', views.create_addBackground, name='create_addBackground'),
    url(r'^account/create/finish/$', views.createAccountFinish, name='createAccountFinish'),
    
    # Create posts
    url(r'^create/event/$', views.createEvent, name='create_event'),

    # Choose type
    url(r'^create/post/choose/$', views.choosePostType, name='choose_postType'),

    # Other
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ajax/$', ajax.call, name='ajax'),
    url(r'^(?P<username>[A-Za-z0-9]+)/$', views.displayProfile, name='displayProfile'),
    url(r'^jobs/$', views.jobs, name='jobs'),
]
