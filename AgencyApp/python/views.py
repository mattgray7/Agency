from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

from django.http import JsonResponse
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
import browse
import post
import helpers

import post_event as eventPost
import post_project as projectPost
import post_collaboration as collaborationPost
import post_work as workPost
import post_casting as castingPost


def returnAjax(request, view, destPageName):
    success = view.processForm()
    destURL = helpers.getDestinationURL(request=request, destPageName=destPageName)
    return JsonResponse({"destURL": destURL, "success": success})

def returnHTTP(view):
    # TODO anything to do here?
    return view.process()

def handleRequest(request, view):
    if request.POST.get("ajax", False):
        return returnAjax(request=request, view=view, destPageName=request.POST.get("next"))
    else:
        return returnHTTP(view=view)

def handleURL(request):
    urlPageName = request.resolver_match.url_name
    view = constants.VIEW_CLASS_MAP.get(urlPageName)(request=request, currentPage=urlPageName)
    return handleRequest(request=request, view=view)

def handleUsernameURL(request, username):
    urlPageName = request.resolver_match.url_name
    view = constants.VIEW_CLASS_MAP.get(urlPageName)(request=request, currentPage=urlPageName, username=username)
    return handleRequest(request=request, view=view)

def handlePostIDURL(request, postID):
    urlPageName = request.resolver_match.url_name
    view = constants.VIEW_CLASS_MAP.get(urlPageName)(request=request, currentPage=urlPageName, postID=postID)
    return handleRequest(request=request, view=view)

def handleEditPostIDURL(request, postID):
    urlPageName = request.resolver_match.url_name
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
        view = constants.VIEW_CLASS_MAP.get(urlPageName)(request=request, currentPage=urlPageName, postID=postID)
    return handleRequest(request=request, view=view)

def handleViewPostIDURL(request, postID):
    urlPageName = request.resolver_match.url_name
    if post.isEventPost(postID):
        view = eventPost.ViewEventPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isProjectPost(postID):
        view = projectPost.ViewProjectPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isCollaborationPost(postID):
        view = collaborationPost.ViewCollaborationPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isWorkPost(postID):
        view = workPost.ViewWorkPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    elif post.isCastingPost(postID):
        view = castingPost.ViewCastingPostView(request=request, currentPage=constants.VIEW_POST, postID=postID)
    else:
        view = constants.VIEW_CLASS_MAP.get(urlPageName)(request=request, currentPage=urlPageName, postID=postID)
    return handleRequest(request=request, view=view)
    

# ============================== Basic pages ================================== #

def login(request):
    view = account.LoginView(request=request, currentPage=constants.LOGIN)
    return view.process()

def logout(request):
    view = account.LogoutView(request=request, currentPage=constants.LOGOUT)
    return view.process()

# ============================================================================= #



# ========================= Create/edit account pages ========================= #

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

def editActorDescription(request):
    view = account.EditActorDescriptionView(request=request, currentPage=constants.EDIT_ACTOR_DESCRIPTION)
    return view.process()

def createAccountFinish(request):
    view = account.CreateAccountFinishView(request=request, currentPage=constants.CREATE_BASIC_ACCOUNT_FINISH)
    return view.process()

# ============================================================================= #



# ============================== Create post pages ============================== #

def createPost(request):
    print request.resolver_match.url_name
    view = post.CreatePostTypesView(request=request, currentPage=constants.CREATE_POST)
    return handleRequest(request, view)

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

# ====================================================================================== #

