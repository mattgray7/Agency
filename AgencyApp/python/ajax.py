import os
import json
from django.http import JsonResponse

import post
import models
import helpers
import constants
import browse
import post_casting as castingPost
import post_work as workPost
import post_event as eventPost



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
    elif postType == "project":
        ret["postID"] = helpers.createUniqueID(destDatabase=models.ProjectPost,
                                                            idKey="postID")
    return JsonResponse(ret)

def createNewCastingPost(request):
    newPost = castingPost.CastingPostInstance(request=request, postID=request.POST.get("postID"), projectID=request.POST.get("projectID"), postType=constants.CREATE_CASTING_POST, formSubmitted=True)
    return _createNewPost(request, newPost)

def createNewWorkPost(request):
    newPost = workPost.WorkPostInstance(request=request, postID=request.POST.get("postID"), projectID=request.POST.get("projectID"), postType=constants.CREATE_WORK_POST, formSubmitted=True)
    return _createNewPost(request, newPost)

def createNewEventPost(request):
    newPost = eventPost.EventPostInstance(request=request, postID=request.POST.get("postID"), projectID=request.POST.get("projectID"), postType=constants.CREATE_EVENT_POST, formSubmitted=True)
    return _createNewPost(request, newPost)

def _createNewPost(request, postTypeInstance):
    createSuccess = postTypeInstance.formIsValid()
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
    return JsonResponse({"success": createSuccess and pictureSuccess, "errors": postTypeInstance.formErrors,
                         "pictureURL": postInstance and postInstance.postPicture and postInstance.postPicture.url or "",
                         "postID": request.POST.get("postID")})

def createUnregisteredProject(request):
    success = False
    postID = request.POST.get("projectID")
    if request.POST.get("name") and request.user.username:
        try:
            projectInstance = models.UnregisteredProject.objects.get(postID=postID)
        except models.UnregisteredProject.DoesNotExist:
            postID = helpers.createUniqueID(destDatabase=models.UnregisteredProject,
                                            idKey="postID")
            projectInstance = models.UnregisteredProject(postID=postID)
            projectInstance.save()

        projectInstance.title = request.POST.get("name")
        projectInstance.poster = request.user.username
        projectInstance.projectType = request.POST.get("type")
        projectInstance.status = request.POST.get("status")
        projectInstance.profession = request.POST.get("profession")
        projectInstance.year = request.POST.get("year")
        projectInstance.save();
        success = True
    return JsonResponse({"success": success, "postID": postID})

def deleteUnregisteredProject(request):
    success = False
    postID = request.POST.get("projectID")
    if postID:
        models.UnregisteredProject.objects.filter(postID=postID).delete()
        success = True;
    return JsonResponse({"success": success})


def _uploadTempPictureToPostDatabase(request):
    success = False
    tempPicture = None
    tempPictureURL = None
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
                    tempPictureURL = str(tempPicture.postPicture.url)
                    postInstance.postPicture = tempPicture.postPicture
                    postInstance.save()
                    success = helpers.savePostPictureInDatabase(request, "postPicture", postInstance, postData.get("cropInfo", {}), postData.get("filename"))
    return {"success": success, "post": postInstance, "tempPictureURL": tempPictureURL}

def editExistingPost(request):
    postID = request.POST.get("postID")
    editSuccess = False
    pictureSuccess = False
    pictureURL = None
    removedPicture = False
    postInstance = None
    if postID:
        postObj = post.getPost(postID)
        if postObj:
            # Save the text values of the form
            createPage = constants.CREATE_POST_PAGE_MAP.get(postObj.postType)
            PostInstanceClass = post.getPostInstanceClass(postID)
            if PostInstanceClass:
                postInstance = PostInstanceClass(request=request, postID=postID, projectID=request.POST.get("projectID"),
                                                 postType=createPage, formSubmitted=True)
                editSuccess = postInstance.formIsValid()

            # If there is a temp picture saved, upload it to this post
            tempPicID = request.POST.get("tempPostPictureID")
            if tempPicID:
                newPicData = _uploadTempPictureToPostDatabase(request)
                pictureSuccess = newPicData.get("success")
                postObj= newPicData.get("post")
                pictureURL = newPicData.get("tempPictureURL")
            else:
                if request.POST.get("removePostPicture") in [True, "True", "true"]:
                    deletePostPicture(request)
                    removedPicture = True
                pictureSuccess = True

    # If no temp picture saved, return the existing pic path
    if not pictureURL:
        pictureURL = postObj and postObj.postPicture and str(postObj.postPicture.url) or None

    return JsonResponse({"success": editSuccess and pictureSuccess, "pictureURL": pictureURL, "postID": postID,
                         "removedPicture": removedPicture, "errors": postInstance and postInstance.formErrors})

def _getCropInfo(request):
    cropInfo = {}
    if request:
        cropInfo = {"x": request.POST.get("crop_x"),
                    "y": request.POST.get("crop_y"),
                    "width": request.POST.get("crop_width"),
                    "height": request.POST.get("crop_height")
                    }
    return cropInfo

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
                "cropInfo": _getCropInfo(request),
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
    tempPostPicture = None
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
    return JsonResponse({"success": success, "tempID": tempID, "pictureURL": tempPostPicture and tempPostPicture.postPicture and tempPostPicture.postPicture.url or ''})

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
            if postObj.postPicture:
                dataDict["postPicture"] = postObj.postPicture and str(postObj.postPicture.url)
            success = True

            # Get participants
            participants = models.PostParticipant.objects.filter(postID=postID)
            participantList = []
            if participants:
                for part in participants:
                    try:
                        user = models.UserAccount.objects.get(username=part.username)
                    except models.UserAccount.DoesNotExist:
                        continue
                    else:
                        newPart = {"username": part.username, "status": part.status,
                                   "publicParticipation": part.publicParticipation,
                                   "profilePictureURL": user.profilePicture and user.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH,
                                   "cleanName": user.cleanName, "profession": user.mainProfession}
                        participantList.append(newPart)
            if participantList:
                dataDict["participants"] = participantList
    return JsonResponse({"success": success, "postData": dataDict})

def saveProfileMediaPicture(request):
    success = False
    username = request.user.username
    newPic = ""
    if username and request.FILES:
        # First 3 are automatically featured
        featured = False
        profilePictures = models.ProfileMediaPicture.objects.filter(username=username)
        if len(profilePictures) < 3:
            featured = True;

        pictureID = helpers.createUniqueID(models.ProfileMediaPicture, "pictureID")
        mediaPicture = models.ProfileMediaPicture(pictureID=pictureID, username=username, featured=featured, description=request.POST.get("otherMediaPictureDescription"))
        success = helpers.savePostPictureInDatabase(request, "otherMediaPictureFile", mediaPicture, _getCropInfo(request), "mediaPicture_{0}.jpg".format(pictureID))
        if success:
            newPic = mediaPicture and mediaPicture.postPicture and mediaPicture.postPicture.url or None
    return JsonResponse({"success": success, "pictureID": pictureID, "pictureURL": newPic, "featured": featured})

def deleteProfileMediaPicture(request):
    pictureID = request.POST.get("pictureID")
    success = False
    if pictureID and request.user.username:
        models.ProfileMediaPicture.objects.filter(pictureID=pictureID).delete()
        success = True
    return JsonResponse({"success": success})

def updateProfileMediaPictureFeaturedStatus(request):
    success = False
    errors = []
    username = request.user.username
    pictureID = request.POST.get("pictureID")
    newFeaturedValue = request.POST.get("isFeatured") in [True, "true", "True"];
    if pictureID and username:
        skipUpdate = False

        # Check if there are already 3 featured photos
        if newFeaturedValue:
            featuredPics = models.ProfileMediaPicture.objects.filter(username=username, featured=True)
            if len(featuredPics) >= 3:
                skipUpdate = True
                errors.append("You can only feature 3 photos.")

        if not skipUpdate:
            try:
                picture = models.ProfileMediaPicture.objects.get(pictureID=pictureID)
            except models.ProfileMediaPicture.DoesNotExist:
                pass
            else:
                picture.featured = newFeaturedValue
                picture.save()
                success = True
    return JsonResponse({"success": success, "errors": errors})

def createProfileEndorsement(request):
    success = False
    postID = None
    username = request.POST.get("username")
    poster = request.user.username
    description = request.POST.get("description")
    if username and poster and description:
        postID = helpers.createUniqueID(models.ProfileEndorsement, "postID")
        endorsement = models.ProfileEndorsement(postID=postID, username=username, poster=poster, description=description)
        endorsement.save()
        success = True
    return JsonResponse({"success": success, "postID": postID})

def updateProfileEndorsement(request):
    success = False
    postID = request.POST.get("postID")
    description = request.POST.get("newDescription")
    if postID and description and request.user.username:
        try:
            endorsement = models.ProfileEndorsement.objects.get(postID=postID)
        except models.ProfileEndorsement.DoesNotExist:
            pass
        else:
            if endorsement.poster == request.user.username:
                endorsement.description = description
                endorsement.save()
                success = True
    return JsonResponse({"success": success})

def deleteProfileEndorsement(request):
    success = False
    postID = request.POST.get("postID")
    profileUsername = request.POST.get("profileUsername")
    if postID and profileUsername and request.user.username:
        try:
            endorsement = models.ProfileEndorsement.objects.get(postID=postID)
        except models.ProfileEndorsement.DoesNotExist:
            pass
        else:
            if endorsement.poster == request.user.username or profileUsername == request.user.username:
                models.ProfileEndorsement.objects.filter(postID=postID).delete()
                success = True
    return JsonResponse({"success": success})

def savePostParticipant(request):
    postID = request.POST.get("postID")
    statusLabel = request.POST.get("status") or "Involved"
    publicParticipation = request.POST.get("publicParticipation") == "true"
    success = False
    matchingUser = None
    if postID:
        participantName = request.POST.get("name").lower()
        if participantName:
            # First search usernames:
            try:
                matchingUser = models.UserAccount.objects.get(username=participantName)
            except models.UserAccount.DoesNotExist:
                # Try first/last names
                if " " in participantName:
                    splitted = participantName.split(" ")
                    if len(splitted) > 1:
                        try:
                            matchingUser = models.UserAccount.objects.get(firstName=splitted[0], lastName=splitted[1])
                        except models.UserAccount.DoesNotExist:
                            pass

            if matchingUser:
                try:
                    existingParticipant = models.PostParticipant.objects.get(postID=postID, username=matchingUser.username)
                except models.PostParticipant.DoesNotExist:
                    # Create it it if it doesn't exist (if it does, TODO update the label?)
                    existingParticipant = models.PostParticipant(postID=postID, username=matchingUser.username, status=statusLabel, publicParticipation=publicParticipation)
                    existingParticipant.save()

                if statusLabel == "Cast":
                    try:
                        postInstance = models.CastingPost.objects.get(postID=postID)
                    except models.CastingPost.DoesNotExist:
                        pass
                    else:
                        postInstance.actorName = matchingUser.username;
                        postInstance.save()
                        print "saved {0} as actor name on post {1}".format(matchingUser.username, postID)
                elif statusLabel == "Hired":
                    try:
                        postInstance = models.WorkPost.objects.get(postID=postID)
                    except models.WorkPost.DoesNotExist:
                        pass
                    else:
                        postInstance.workerName = matchingUser.username;
                        postInstance.save()


                success = True


    return JsonResponse({"success": success, "user": matchingUser and {"username": matchingUser.username,
                                                                       "cleanName": matchingUser.cleanName,
                                                                       "profilePictureURL": matchingUser.profilePicture and matchingUser.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH,
                                                                       "profession": matchingUser.mainProfession,
                                                                       "status": statusLabel,
                                                                       "publicParticipation": publicParticipation}})

def deletePostParticipant(request):
    postID = request.POST.get("postID")
    username = request.POST.get("username")
    success = False
    if postID and username:
        matches = models.PostParticipant.objects.filter(postID=postID, username=username)
        if matches:
            matches.delete()
            success = True
    return JsonResponse({"success": success, "user": {"username": username}})

def _userDoesExist(username):
    try:
        user = models.UserAccount.objects.get(username=username)
        return True
    except models.UserAccount.DoesNotExist:
        pass
    return False

def _postDoesExist(postID):
    if post.getPost(postID):
        return True
    return False

def saveProjectAdmin(request):
    projectID = request.POST.get("projectID")
    username = request.POST.get("username")
    success = False
    if projectID and username:
        if _postDoesExist(projectID):
            if _userDoesExist(username):
                # User and project are valid, so can save admin
                try:
                    admin = models.ProjectAdmin.objects.get(projectID=projectID, username=username)
                except models.ProjectAdmin.DoesNotExist:
                    admin = models.ProjectAdmin(projectID=projectID, username=username)
                    admin.save()
                    success = True
    return JsonResponse({"success": success})

def deleteProjectAdmin(request):
    projectID = request.POST.get("projectID")
    username = request.POST.get("username")
    success = False
    if projectID and username:
        if _postDoesExist(projectID):
            if _userDoesExist(username):
                print "deleting admin {0}".format(username)
                models.ProjectAdmin.objects.filter(projectID=projectID, username=username).delete()
                success = True
    return JsonResponse({"success": success})

def updatePostParticipationPrivacy(request):
    postID = request.POST.get("postID")
    username = request.POST.get("username")
    privacyValue = request.POST.get("value") == "true";
    success = False
    if postID and username:
        try:
            part = models.PostParticipant.objects.get(postID=postID, username=username)
        except models.PostParticipant.DoesNotExist:
            pass
        else:
            part.publicParticipation = privacyValue
            part.save()
            success = True
    return JsonResponse({"success": success})

def updatePostParticipationStatus(request):
    postID = request.POST.get("postID")
    username = request.POST.get("username")
    statusValue = request.POST.get("value")
    success = False
    if postID and username:
        try:
            part = models.PostParticipant.objects.get(postID=postID, username=username)
        except models.PostParticipant.DoesNotExist:
            pass
        else:
            part.status = statusValue
            part.save()
            success = True
    return JsonResponse({"success": success})

def getSearchPreviewUsers(request):
    text = request.POST.get("text")
    success = False
    returnList = []
    matchingUsers = None
    if text:
        if " " in text:
            splitted = text.split(" ")
            if len(splitted) >= 2:
                matchingUsers = models.UserAccount.objects.filter(firstName__icontains=splitted[0],
                                                                   lastName__icontains=splitted[1])
        if not matchingUsers:
            matchingUsers = models.UserAccount.objects.filter(username__icontains=text)
        if matchingUsers:
            success = True
            returnList = [{"username": x.username, "cleanName": x.cleanName, "profession": x.mainProfession,
                           "profilePicture": x.profilePicture and x.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH} for x in matchingUsers]
    return JsonResponse({"success": success, "users": returnList})

def getSearchPreviewProfessions(request):
    text = request.POST.get("text")
    returnList = []
    for profession in constants.PROFESSION_LIST:
        if profession.lower().startswith(text.lower()):
            returnList.append(profession)
    return JsonResponse({"success": True, "professions": sorted(returnList)})

def getSearchSuggestions(request):
    searchValue = request.POST.get("text")
    suggestions = {}
    if searchValue:
        # Get professions, projects, users

        # Get professions
        professionList = []
        for category in constants.PROFESSIONS:
            for profession in constants.PROFESSIONS[category]:
                if profession.lower().startswith(searchValue.lower()):
                    professionList.append(profession)
        if professionList:
            suggestions["Profession"] = list(set(professionList))      # Remove duplicates

        # Get projects
        projects = ([x.title for x in models.ProjectPost.objects.filter(title__contains=searchValue)] +
                    [x.title for x in models.ProjectPost.objects.filter(title__contains="The {0}".format(searchValue))])
        if projects:
            suggestions["Project"] = list(set(projects))

        # Get users
        users = None
        if " " in searchValue:
            splitted = searchValue.split(" ")
            if len(splitted) > 1:
                users = models.UserAccount.objects.filter(firstName=splitted[0], lastName__startswith=splitted[1])
        if not users:
            users = models.UserAccount.objects.filter(firstName__startswith=searchValue)
        if users:
            suggestions["User"] = [{"username": x.username, "cleanName": x.cleanName,
                                    "profession": x.mainProfession or "User"} for x in users]
    return JsonResponse({"success": True, "suggestions": suggestions})

def getSearchResults(request):
    searchValue = request.POST.get("searchValue")
    categories = request.POST.getlist("categories[]")       # Need the brackets to convert js array to python list
    numResults = int(request.POST.get("numResults", 3))
    filters = json.loads(request.POST.get("filters"))
    results = {}
    if len(categories) > 0:
        for category in categories:
            if category not in results:
                results[category] = {"results": [], "moreResults": False, "numResults": 0}
            if category == "jobs":
                results[category] = browse.getJobsSearchResults(searchValue, numResults, filters.get("jobs"))
            elif category == "roles":
                results[category] = browse.getRolesSearchResults(searchValue, numResults, filters.get("roles"))
            elif category == "projects":
                results[category] = browse.getProjectSearchResults(searchValue, numResults, filters.get("projects"))
            elif category == "events":
                results[category] = browse.getEventSearchResults(searchValue, numResults, filters.get("events"))
            elif category == "users":
                results[category] = browse.getUserSearchResults(searchValue, numResults, filters.get("users"))
    return JsonResponse({"success": True, "results": results})


def sendNewMessage(request):
    success = False
    messageID = None
    conversationID = None
    sender = request.POST.get("sender")
    recipient = request.POST.get("recipient")
    content = request.POST.get("content")
    if sender and sender == request.user.username:
        if recipient:
            try:
                recipientUser = models.UserAccount.objects.get(username=recipient)
            except models.UserAccount.DoesNotExist:
                pass
            else:
                success = _sendMessage(sender, recipient, content)
    return JsonResponse({"success": success, "messageID": messageID})

def _sendMessage(sender, recipient, content, application=False):
    success = False
    if content:
        # Message is valid, check if there is a conversation already started between 2 users
        conversationID = None
        conversations1 = models.Conversation.objects.filter(user1=sender, user2=recipient)
        conversations2 = models.Conversation.objects.filter(user1=recipient, user2=sender)
        if conversations1 or conversations2:
            if conversations1 and len(conversations1) == 1:
                conversationID = conversations1[0].conversationID
            elif conversations2 and len(conversations2) == 1:
                conversationID = conversations2[0].conversationID
        if not conversationID:
            conversationID = helpers.createUniqueID(destDatabase=models.Conversation,
                                                    idKey="conversationID")
            conversation = models.Conversation(conversationID=conversationID, user1=sender, user2=recipient)
            conversation.save()

        if conversationID:
            messageID = helpers.createUniqueID(destDatabase=models.Message,
                                               idKey="messageID")
            message = models.Message(messageID=messageID,
                                     conversationID=conversationID,
                                     sender=sender,
                                     recipient=recipient,
                                     content=content,
                                     applicationMessage=application)
            message.save()
            success = True
        return success

def getConversation(request):
    success = False
    conversationID = request.POST.get("conversationID")
    conversationList = []
    userDict = {}
    if conversationID:
        try:
            conversation = models.Conversation.objects.get(conversationID=conversationID)
        except models.Conversation.DoesNotExist:
            pass
        else:

            try:
                user1 = models.UserAccount.objects.get(username=conversation.user1)
                user2 = models.UserAccount.objects.get(username=conversation.user2)
            except models.UserAccount.DoesNotExist:
                pass
            else:
                userDict[user1.username] = {"username": user1.username,
                                            "cleanName": user1.cleanName,
                                            "profileProfessions": user1.mainProfession,
                                            "profilePictureURL": user1.profilePicture and user1.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH}
                userDict[user2.username] = {"username": user2.username,
                                            "cleanName": user2.cleanName,
                                            "profileProfessions": user2.mainProfession,
                                            "profilePictureURL": user2.profilePicture and user2.profilePicture.url or constants.NO_PROFILE_PICTURE_PATH}

                for message in conversation.messages:
                    if message.applicationMessage:
                        if message.sender == request.user.username:
                            # Don't display user's applications in message thread
                            continue

                    conversationList.append({"messageID": message.messageID,
                                             "sender": message.sender,
                                             "recipient": message.recipient,
                                             "unread": not message.recipientSeen,
                                             "content": message.content,
                                             "sentTime": message.sentTime.strftime("%s"),
                                             "applicationMessage": message.applicationMessage
                                             })
            success = True
    return JsonResponse({"success": success, "conversation": {"users": userDict, "messages": conversationList}})

def updateMessageUnread(request):
    success = False
    messageID = request.POST.get("messageID")
    unread = request.POST.get("unread") == "true"
    if messageID:
        try:
            message = models.Message.objects.get(messageID=messageID)
        except models.Message.DoesNotExist:
            pass
        else:
            try:
                convo = models.Conversation.objects.get(conversationID=message.conversationID)
            except models.Conversation.DoesNotExist:
                pass
            else:
                for convoMessage in convo.messages:
                    if convoMessage.recipient == request.user.username:
                        convoMessage.recipientSeen = not unread
                        convoMessage.save()
                success = True
    return JsonResponse({"success": success})

def submitNewApplication(request):
    success = False
    applicantUsername = request.POST.get("applicant")
    postID = request.POST.get("postID")
    if applicantUsername and postID:
        try:
            applicant = models.UserAccount.objects.get(username=applicantUsername)
        except models.UserAccount.DoesNotExist:
            pass
        else:
            destPost = post.getPost(postID)
            if destPost:
                messageContent = "<a onclick='redirectToUser(\"{0}\");'>{1}</a> submitted an application for your post <a onclick='redirectToPost(\"{2}\");'>{3}</a>.".format(applicantUsername, applicant.cleanName, postID, destPost.title)

                if request.POST.get("content"):
                    messageContent = messageContent + "\n\n{0} added this message:\n{1}".format(applicant.firstName, request.POST.get("content"))

                if applicant.resume:
                    messageContent = messageContent + "\n\nView {0}'s <a onclick='redirectToUser(\"{1}\");'>profile</a>, or go straight to the <a href='/media/{2}'>resume</a>.".format(applicant.firstName, applicantUsername, applicant.resume)

                success = _sendMessage(applicantUsername, destPost.poster, messageContent, application=True)
    return JsonResponse({"success": success})


