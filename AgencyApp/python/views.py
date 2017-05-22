from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import constants
import helpers
import models

import os
import simplejson as json

# Must be done after GenericView defined
import genericViews as views
import home
import profile
import account
import browse as browseModule   # to avoid conflict with browse method
import post

import post_event as eventPost
import post_project as projectPost
import post_collaboration as collaborationPost
import post_work as workPost
import post_casting as castingPost


def displayHome(request):
    view = home.HomeView(request=request, currentPage=constants.HOME)
    return view.process()

def login(request):
    view = account.LoginView(request=request, currentPage=constants.LOGIN)
    return view.process()

def logout(request):
    view = account.LogoutView(request=request, currentPage=constants.LOGOUT)
    return view.process()

def createAccount(request):
    view = account.CreateAccountView(request=request, currentPage=constants.CREATE_BASIC_ACCOUNT)
    return view.process()

def editInterests(request):
    view = account.EditInterestsView(request=request, currentPage=constants.EDIT_INTERESTS)
    return view.process()

def editProfessions(request):
    view = account.EditProfessionsView(request=request, currentPage=constants.EDIT_PROFESSIONS)
    return view.process()

def editPicture(request):
    view = account.EditPictureView(request=request, currentPage=constants.EDIT_PROFILE_PICTURE)
    return view.process()

def editBackground(request):
    view = account.EditBackgroundView(request=request, currentPage=constants.EDIT_BACKGROUND)
    return view.process()

def createAccountFinish(request):
    view = account.CreateAccountFinishView(request=request, currentPage=constants.CREATE_BASIC_ACCOUNT_FINISH)
    return view.process()

def createPostChoice(request):
    view = post.CreatePostChoiceView(request=request, currentPage=constants.CREATE_POST_CHOICE)
    return view.process()

def createEventPost(request):
    view = eventPost.CreateEventPostView(request=request, currentPage=constants.CREATE_EVENT_POST)
    return view.process()

def createProjectPost(request):
    view = projectPost.CreateProjectPostView(request=request, currentPage=constants.CREATE_PROJECT_POST)
    return view.process()

def createCollaborationPost(request):
    view = collaborationPost.CreateCollaborationPostView(request=request, currentPage=constants.CREATE_COLLABORATION_POST)
    return view.process()

def createWorkPost(request):
    view = workPost.CreateWorkPostView(request=request, currentPage=constants.CREATE_WORK_POST)
    return view.process()

def createCastingPost(request):
    view = castingPost.CreateCastingPostView(request=request, currentPage=constants.CREATE_CASTING_POST)
    return view.process()

def createPost(request):
    view = post.CreatePostTypesView(request=request, currentPage=constants.CREATE_POST)
    return view.process()

def editPost(request, postID):
    if post.isEventPost(postID):
        view = eventPost.CreateEventPostView(request=request, currentPage=constants.EDIT_POST, postID=postID)
    elif post.isCollaborationPost(postID):
        view = collaborationPost.CreateCollaborationPostView(request=request, currentPage=constants.EDIT_POST, postID=postID)
    elif post.isWorkPost(postID):
        view = workPost.CreateWorkPostView(request=request, currentPage=constants.EDIT_POST, postID=postID)
    elif post.isProjectPost(postID):
        view = projectPost.CreateProjectPostView(request=request, currentPage=constants.EDIT_POST, postID=postID)
    elif post.isCastingPost(postID):
        view = castingPost.CreateCastingPostView(request=request, currentPage=constants.EDIT_POST, postID=postID)
    else:
        print "ERROR SELECTING EDIT POST VIEW"
        raise
    return view.process()

def viewPost(request, postID):
    if post.isEventPost(postID):
        view = eventPost.ViewEventPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isCollaborationPost(postID):
        view = collaborationPost.ViewCollaborationPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isWorkPost(postID):
        view = workPost.ViewWorkPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isProjectPost(postID):
        view = projectPost.ViewProjectPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isCastingPost(postID):
        view = castingPost.ViewCastingPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    else:
        print "ERROR SELECTING EDIT VIEW POST VIEW"
        raise
    return view.process()

def browse(request, browseType=constants.BROWSE):
    view = browseModule.BrowseView(request=request, currentPage=browseType)
    return view.process()

def browseEvents(request):
    return browse(request, browseType=constants.BROWSE_EVENTS)

def browseProjects(request):
    return browse(request, browseType=constants.BROWSE_PROJECTS)

def browseCollaborationPosts(request):
    return browse(request, browseType=constants.BROWSE_COLLABORATION_POSTS)

def browseWorkPosts(request):
    return browse(request, browseType=constants.BROWSE_WORK_POSTS)

def browsePosts(request):
    return browse(request, browseType=constants.BROWSE_POSTS)

def displayProfile(request, username):
    view = profile.ProfileView(request=request, username=username, currentPage=constants.PROFILE)
    return view.process()

def jobs(request):
    return render(request, 'AgencyApp/jobs.html', {'jobList': ['job1', 'job2', 'job3']})