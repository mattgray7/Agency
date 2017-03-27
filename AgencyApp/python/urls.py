import ajax
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create/$', views.createAccount, name='createAccount'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ajax/$', ajax.call, name='ajax'),
    url(r'^(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    url(r'^jobs/$', views.jobs, name='jobs'),
]
