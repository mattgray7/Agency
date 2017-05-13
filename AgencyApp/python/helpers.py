from django.contrib import messages

from django.http import HttpResponseRedirect
import constants
import random, string



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
    destinationURL = getDestinationURL(request, destinationPage)
    if not destinationURL:
        print "No url could be resolved"
        raise
    else:
        messages.add_message(request, messages.INFO,
                             "source:{0}".format(currentPage))
        return HttpResponseRedirect(destinationURL)


def getDestinationURL(request, destPageName):
    destURL = constants.URL_MAP.get(destPageName)

    # Add specific values for profile usernames and eventIDs in the url
    if destPageName == constants.PROFILE:
        if request.user.username:
            destURL = destURL.format(request.user.username)
        else:
            print "NO USERNAME PASSED TO getDestinationURL"
    elif destPageName in [constants.VIEW_POST, constants.CREATE_EVENT_POST, constants.CREATE_COLLABORATION_POST,
                          constants.CREATE_WORK_POST, constants.CREATE_PROJECT_POST,
                          constants.EDIT_POST]:
        if request.POST.get('postID'):
            destURL = destURL.format(request.POST.get('postID'))
            messages.add_message(request, messages.INFO,
                                 "postID:{0}".format(request.POST.get('postID')))
        else:
            print "NO POSTID PASSED TO getDestinationURL"
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
    return {"toolbarDestinations": {"login": constants.LOGIN,
                                     "home": constants.HOME,
                                     "logout": constants.LOGOUT,
                                     "profile": constants.PROFILE,
                                     "browse": constants.BROWSE},
            "source": source,
            "default": constants.DEFAULT,
            "cancel": constants.CANCEL
            }


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
