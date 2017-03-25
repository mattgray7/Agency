from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # ex: /polls/5/
    # TODO Use regex or syntax for caps, lowercase, and numbers
    url(r'^user/(?P<username>[a-z]+)/$', views.profile, name='profile'),
    # ex: /polls/5/results/
    url(r'^jobs/$', views.jobs, name='jobs'),
]
