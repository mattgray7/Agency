import os
from django.http import JsonResponse

import post
import models
import helpers
import constants
import post_casting as castingPost


def followPost(request, postID):
    if post.isFollowingPost(postID, request.user.username):
        success = post.unfollowPost(postID=postID, username=request.user.username)
    else:
        success = post.followPost(postID=postID, username=request.user.username)
    return JsonResponse({"success": success})


def getPostFollowingBool(request):
    return JsonResponse({"following": isFollowingPost(request.POST.get("postID"),
                                                      username=request.user.username)})


def getUserProjects(request):
    if request.user.username:
        projects = []
        for project in models.ProjectPost.objects.filter(poster=request.user.username):
            projects.append({"projectID": project.postID, "projectName": project.title})
        return JsonResponse({"projects": projects})


def deletePostFromDB(request):
    postID = request.POST.get("postID")
    postType = request.POST.get("postType")
    success = False
    errors = []
    if not postID or not postType:
        errors.append("Could not delete post with info postID:{0} and postType:{1}".format(postID, postType))
    else:
        postDB = constants.POST_DATABASE_MAP.get(postType)
        if not postDB:
            errors.append("Could not determine post database from type {0}".format(postType))
        else:
            postDB.objects.filter(postID=postID).delete()
            success = True
    return JsonResponse({"success": success, "errors": errors})


def deleteProfilePicture(request):
    if request.user.is_authenticated:
        try:
            userAccount = models.UserAccount.objects.get(username=request.user.username)
        except models.UserAccount.DoesNotExist:
            pass
        else:
            if userAccount.profilePicture:
                picturePath = userAccount.profilePicture.path
                userAccount.profilePicture = None
                userAccount.save()
                os.remove(picturePath)
    return JsonResponse({"success": True})

def deletePostPicture(request):
    success = False
    postID = request.POST.get("postID")
    if postID:
        database = post.getPostDatabase(postID)
        if database:
            try:
                postInstance = database.objects.get(postID=postID)
            except database.DoesNotExist:
                pass
            else:
                postInstance.postPicture = None
                postInstance.save()
                success = True
    return JsonResponse({"success": success})


def getNewPostID(request):
    postType = request.POST.get("postType")
    ret = {}
    if postType == "casting":
        ret["postID"] = helpers.createUniqueID(destDatabase=models.CastingPost,
                                                            idKey="postID")
    elif postType == "work":
        ret["postID"] = helpers.createUniqueID(destDatabase=models.WorkPost,
                                                            idKey="postID")
    elif postType == "event":
        ret["postID"] = helpers.createUniqueID(destDatabase=models.EventPost,
                                                            idKey="postID")
    return JsonResponse(ret)

def createNewCastingPost(request):
    newPost = castingPost.CastingPostInstance(request=request, postID=request.POST.get("postID"), projectID=request.POST.get("projectID"), postType=constants.CREATE_CASTING_POST, formSubmitted=True)
    createSuccess = newPost.formIsValid()
    return JsonResponse({"success": createSuccess})

def updatePostPicture(request):
    postID = request.POST.get("postID")
    database = post.getPostDatabase(postID)
    filename = constants.MEDIA_FILE_NAME_MAP.get(request.POST.get("postType"), "tempfile_{0}").format(postID)
    success = False
    if postID and database:
        try:
            postInstance = database.objects.get(postID=postID)
        except database.DoesNotExist:
            pass
        else:
            cropInfo = {"x": request.POST.get("crop_x"),
                        "y": request.POST.get("crop_y"),
                        "width": request.POST.get("crop_width"),
                        "height": request.POST.get("crop_height")}
            success = helpers.savePostPictureInDatabase(request, "postPicture", postInstance, cropInfo, filename)
    return JsonResponse({"success": success})

def saveTempPostPicture(request):
    tempID = helpers.createUniqueID(models.TempPostPicture, "tempID")
    success = False
    if tempID:
        try:
            tempPostPicture = models.TempPostPicture.objects.get(tempID=tempID)
        except models.TempPostPicture.DoesNotExist:
            # Create the db instance
            tempPostPicture = models.TempPostPicture(tempID=tempID, username=request.user.username)
            tempPostPicture.save()

            # Save the picture with the crop
            cropInfo = {"x": request.POST.get("crop_x"),
                        "y": request.POST.get("crop_y"),
                        "width": request.POST.get("crop_width"),
                        "height": request.POST.get("crop_height")}
            success = helpers.savePostPictureInDatabase(request, "postPicture", tempPostPicture, cropInfo, "tempPostPicture_{0}.jpg".format(tempID))
    return JsonResponse({"success": success, "tempID": tempID, "pictureURL": tempPostPicture.postPicture.url})



