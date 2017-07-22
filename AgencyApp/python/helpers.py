from django.contrib import messages

from django.http import HttpResponseRedirect
import constants
import random, string
import models
import json
import os
from PIL import Image

def redirect(request, currentPage, destinationPage):
    """Returns an HttpResonseRedirect of the desired URL can be resolved (see getDestinationURL for 
    more info on how this is done). If no URL can be resolved, an error is raised

    :param request: The request object
    :param str currentPage: Current page name as defined in constants.py
    :param str sourcePage: Name of page that led to the current page as defined in constants.py
    :param str pageKey: Optional argument if multiple destinations exist from the same current/source
                        page combintaion, defaults to DEFAULT
    :return HttpResonseRedirect: Redirect to destination if found
    """
    destinationURL = getDestinationURL(request, destinationPage, currentPage)
    if not destinationURL:
        print "No url could be resolved"
        raise
    else:
        messages.add_message(request, messages.INFO,
                             "source:{0}".format(currentPage))
        return HttpResponseRedirect(destinationURL)


def getDestinationURL(request, destPageName, currentPageName=None):
    destURL = constants.URL_MAP.get(destPageName)

    # Add specific values for profile usernames and eventIDs in the url
    if destPageName == constants.PROFILE:
        username = request.POST.get('profileName', request.POST.get('username', request.user.username))
        if username:
            destURL = destURL.format(username)
            messages.add_message(request, messages.INFO,
                                 "profileName:{0}".format(username))
    if request.POST.get('postID'):
        postID = request.POST.get("postID")

        # Cancel from editing casting/work post to skip directly back to the project
        if destPageName == constants.VIEW_POST and request.POST.get(constants.CANCEL) == "True":
            if request.POST.get("skipToProject", False):
                if request.POST.get("projectID"):
                    postID = request.POST.get("projectID")
                else:
                    destPageName = constants.HOME
        destURL = destURL.format(postID)
        messages.add_message(request, messages.INFO,
                             "postID:{0}".format(postID))
    if request.POST.get('projectID'):
        messages.add_message(request, messages.INFO,
                             "projectID:{0}".format(request.POST.get('projectID')))
        if not request.POST.get('postID'):
            messages.add_message(request, messages.INFO,
                                 "postID:{0}".format(request.POST.get('projectID')))
    return destURL


def getDestinationPage(request, currentPage, sourcePage, destPageKey=None):
    """Returns a destination URL taken from the PAGE_MAP dict declared in constants.py.
    The URL is determined from the current page requesting the URL, and the source page
    that led to the current page. If there could be multiple, different destinations from
    the same currentPage and sourcePage, the pageKey is used to determine the correct one. 
    Otherwise, the default page for the current/source combo is used

    :param str currentPage: Current page name as defined in constants.py
    :param str sourcePage: Name of page that led to the current page as defined in constants.py
    :param str destPageKey: Optional argument if multiple destinations exist from the same current/source
                        page combintaion, defaults to DEFAULT
    :param str username: Optional argument if the destination could be profile requiring a username
    :return str: Relative URL defined in the URL_MAP in constants.py
    """
    if None in [currentPage, sourcePage]:
        print "Current or source page not specified"
        #TODO raise proper exception
        raise

    if not destPageKey:
        destPageKey = constants.DEFAULT

    currentPageMap = constants.PAGE_MAP.get(currentPage)
    if currentPageMap:
        if sourcePage == constants.VIEW_EVENT:
            sourcePage = sourcePage.format(request.POST.get("eventID"))
        destPageMap = currentPageMap.get(sourcePage)
        if destPageMap:
            destPageName = destPageMap.get(destPageKey)
            if destPageName:
                return destPageName
                destURL = constants.URL_MAP.get(destPageName)
                # Special case for profile
            else:
                print "helpers.py: getDestinationURL: no destPageName found"
        else:
            print "helpers.py: getDestinationURL: no destPageMap found"
    else:
        print "helpers.py: getDestinationURL: no currentPageMap found"


def getBaseContext(request):
    """Returns context required by the base template.

    :return dict: Context required by base.html
    """
    if request.POST:
        source = request.POST.get("source")
    else:
        source = getMessageFromKey(request, "source")
    returnDict = {"toolbarDestinations": {"login": constants.LOGIN,
                                         "home": constants.HOME,
                                         "logout": constants.LOGOUT,
                                         "profile": constants.PROFILE,
                                         "browse": constants.BROWSE_CHOICE,
                                         "post": constants.CREATE_POST},
                "source": source,
                "default": constants.DEFAULT,
                "cancel": constants.CANCEL,
                "images": {"noProfilePicture": constants.NO_PROFILE_PICTURE_PATH,
                           "noPicture": constants.NO_PICTURE_PATH}
                }
    returnDict["posterNameMap"] = {}
    for account in models.UserAccount.objects.all():
        returnDict["posterNameMap"][account.username] = capitalizeName("{0} {1}".format(account.firstName, account.lastName))
    returnDict["posterNameMap"] = json.dumps(returnDict["posterNameMap"])
    return returnDict


def isPostPage(pageName):
    """Returns True if the pageName is a page dealing with posts

    :param str pageName: The page enum to check
    :return bool: True if the page name is a post page
    """
    return pageName in [constants.VIEW_POST, constants.CREATE_EVENT_POST,
                        constants.CREATE_COLLABORATION_POST, constants.CREATE_WORK_POST,
                        constants.CREATE_PROJECT_POST, constants.EDIT_POST,
                        constants.CREATE_CASTING_POST]


def createUniqueID(destDatabase, idKey):
    """Creates a random alphanumeric id the length of constants.RANDOM_ID_LENGTH. It is
    then checked against the destDatabase to see if it is takesn. If so, a new random id
    is generated and checked until a unique id is found and returned.

    :param models.Model destDatabase: The database to check the uniqueness of generated ID against
    :param str idKey: The name of the id field in the dest database
    """
    tempIDValid = False
    while not tempIDValid:
        tempID = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(constants.RANDOM_ID_LENGTH))
        if len(destDatabase.objects.filter(**{'{0}__contains'.format(idKey): tempID})) == 0:
            tempIDValid = True
            return tempID


def savePostPictureInDatabase(request, pictureFieldName, databaseInstance, cropInfo, filename):
    if databaseInstance:
        databaseInstance.postPicture = request.FILES.get(pictureFieldName)
        databaseInstance.save()

        if databaseInstance.postPicture:
            if cropInfo:
                image = Image.open(databaseInstance.postPicture.path)
                x = float(cropInfo.get("x"))
                y = float(cropInfo.get("y"))
                croppedImage = image.crop((x, y, float(cropInfo["width"]) + x, float(cropInfo["height"]) + y))
                croppedImage.save(databaseInstance.postPicture.path)
                croppedImage = croppedImage.resize((810, 900), Image.ANTIALIAS)
                croppedImage.save(databaseInstance.postPicture.path)

                # Rename picture file
                newPath = os.path.join(os.path.dirname(databaseInstance.postPicture.path), filename)
                os.rename(databaseInstance.postPicture.path, newPath)
                databaseInstance.postPicture.name = os.path.join(request.user.username, filename)
                databaseInstance.save()
            return True
    return False

def getMessageFromKey(request, key):
    """Returns the value of a key included in a message object.

    :param WSGIRequest request: The request to get the message from
    :param str key: The key to return the value for
    :return: The value of the key, None if key doesn't exist
    """
    messagesList = messages.get_messages(request)
    for message in messagesList:
    	# TODO convert unicode messages.messages to dict
    	splitted = message.message.split(":")
        if splitted[0] == key:
            return splitted[1]
    return None


def capitalizeName(name):
    """Capitalizes first letter of names (eg matt gray->Matt Gray, smith-pelly->Smith-Pelly, 
       deBrincat->DeBrincat)

    :param str name: The name to capitalize
    :return str: The capitalized name
    """
    finalName = ''
    first = True
    for char in name:
        if first:
            finalName += char.upper()
            first = False
        elif char in ['-', ' ']:
            finalName += char
            first=True
        else:
            finalName += char
    return finalName
