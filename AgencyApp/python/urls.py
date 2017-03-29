import ajax
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home, name='home'),

    # Create account
    url(r'^create/basic/$', views.create_account, name='create_account'),
    url(r'^create/interests/$', views.create_selectInterests, name='create_selectInterests'),
    url(r'^create/professions/$', views.create_selectProfessions, name='create_selectProfessions'),
    url(r'^create/background/$', views.create_addBackground, name='create_addBackground'),
    url(r'^create/finish/$', views.create_finish, name='create_finish'),
    
    # Create posts
    url(r'^create/event/$', views.create_event, name='create_event'),

    # Choose type
    url(r'^create/post/choose/$', views.choose_postType, name='choose_postType'),

    # Other
    url(r'^browse$', views.browse, name='browse'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ajax/$', ajax.call, name='ajax'),
    url(r'^(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    url(r'^jobs/$', views.jobs, name='jobs'),
]
