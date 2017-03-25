from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create/$', views.createProfile, name='createProfile'),
    url(r'^ajax/getWelcomeMsg/$', views.getWelcomeMsg, name='getWelcomeMsg'),
    # ex: /polls/5/
    # TODO Use regex or syntax for caps, lowercase, and numbers
    url(r'^(?P<username>[A-Za-z0-9]+)/$', views.profile, name='profile'),
    # ex: /polls/5/results/
    url(r'^jobs/$', views.jobs, name='jobs'),
]
