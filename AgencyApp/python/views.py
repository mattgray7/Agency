from django.http import JsonResponse

import constants
import helpers
import os
import simplejson as json

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

