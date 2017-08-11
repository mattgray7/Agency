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
    pictureSuccess = False
    postInstance = None
    if createSuccess:
        newPicData = _uploadTempPictureToPostDatabase(request)
        postInstance = newPicData.get("post")
        if request.POST.get("tempPostPictureID"):
            pictureSuccess = newPicData.get("success")
        else:
            pictureSuccess = True
    else:
        pictureSuccess = True
    return JsonResponse({"success": createSuccess and pictureSuccess, "errors": newPost.formErrors,
                         "pictureURL": postInstance and postInstance.postPicture and postInstance.postPicture.url or ""})

def _uploadTempPictureToPostDatabase(request):
    success = False
    postInstance = post.getPost(request.POST.get("postID"));
    if postInstance:
        tempPostPictureID = request.POST.get("tempPostPictureID")
        if tempPostPictureID:
            try:
                tempPicture = models.TempPostPicture.objects.get(tempID=tempPostPictureID)
            except models.TempPostPicture:
                pass
            else:
                postData = _getPostPictureRequestData(request)
                if tempPicture and tempPicture.postPicture and postData:
                    print tempPicture
                    print tempPicture.postPicture
                    postInstance.postPicture = tempPicture.postPicture
                    postInstance.save()
                    success = helpers.savePostPictureInDatabase(request, "postPicture", postInstance, postData.get("cropInfo", {}), postData.get("filename"))
    return {"success": success, "post": postInstance, "tempPictureURL": tempPicture and tempPicture.postPicture and tempPicture.postPicture.url}

def editExistingPost(request):
    postID = request.POST.get("postID")
    editSuccess = False
    pictureSuccess = False
    pictureURL = None
    if postID:
        postObj = post.getPost(postID)
        if postObj:
            for key in postObj.__dict__:
                if not key.startswith("_"):
                    newValue = request.POST.get(key, None)
                    oldValue = postObj.__dict__[key]
                    if not newValue:
                        if oldValue in ["True", "False"]:
                            newValue = False
                            oldValue = bool(oldValue)
                    else:
                        if newValue != oldValue:
                            print "key {0} has diff values: old={1}, new={2}".format(key, oldValue, newValue)
                            postObj.__dict__[key] = newValue
            postObj.save()
            editSuccess = True
            
            newPicData = _uploadTempPictureToPostDatabase(request)
            postInstance = newPicData.get("post")
            if request.POST.get("tempPostPictureID"):
                pictureSuccess = newPicData.get("success")
            else:
                pictureSuccess = True
            tempPictureURL = newPicData.get("tempPictureURL")
            if tempPictureURL:
                print "HERE doing temp"
                pictureURL = tempPictureURL
            else:
                print "doing post instance"
                pictureURL = postInstance and postInstance.postPicture and postInstance.postPicture.url

    print "pictureURL IS {0}".format(pictureURL)
    return JsonResponse({"success": editSuccess and pictureSuccess, "pictureURL": pictureURL})


def _getPostPictureRequestData(request):
    data = {}
    postID = request.POST.get("postID")
    if postID:
        postType = request.POST.get("postType")
        if not postType:
            postObj = post.getPost(postID)
            if postObj:
                postType = postObj.postType

        data = {"postID": postID,
                "database": post.getPostDatabase(postID),
                "filename": constants.MEDIA_FILE_NAME_MAP.get(postType, "tempfile_{0}").format(postID),
                "cropInfo": {"x": request.POST.get("crop_x"),
                             "y": request.POST.get("crop_y"),
                             "width": request.POST.get("crop_width"),
                             "height": request.POST.get("crop_height")
                             }
                }
        if None in data["cropInfo"].values():
            data["cropInfo"] = {}
    return data


def updatePostPicture(request):
    postData = _getPostPictureRequestData(request)
    postID = postData.get("postID")
    database = postData.get("database")
    success = False
    postInstance = None
    if postID and database:
        try:
            postInstance = database.objects.get(postID=postID)
        except database.DoesNotExist:
            pass
        else:
            success = helpers.savePostPictureInDatabase(request, "postPicture", postInstance, postData.get("cropInfo"), postData.get("filename"))
    return JsonResponse({"success": success, "pictureURL": postInstance and postInstance.postPicture and postInstance.postPicture.url})

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

def getPostData(request):
    """Return a key:value dict of a single post, postID should be passed in request"""
    postID = request.POST.get("postID")
    success = False
    dataDict = {}
    if(postID):
        postObj = post.getPost(postID)
        if postObj:
            for key in postObj.__dict__:
                # Skip hidden attributes
                if not key.startswith("_"):
                    dataDict[key] = postObj.__dict__[key]

            dataDict["postPicture"] = postObj and postObj.postPicture and postObj.postPicture.url
            success = True

    return JsonResponse({"success": success, "postData": dataDict})


