from django.contrib import messages
from django.http import HttpResponseRedirect
import constants


def redirect(request, currentPage, sourcePage, pageKey=None):
    """Returns an HttpResonseRedirect of the desired URL can be resolved (see getDestinationURL for 
    more info on how this is done). If no URL can be resolved, an error is raised

    :param request: The request object
    :param str currentPage: Current page name as defined in constants.py
    :param str sourcePage: Name of page that led to the current page as defined in constants.py
    :param str pageKey: Optional argument if multiple destinations exist from the same current/source
                        page combintaion, defaults to DEFAULT
    :return HttpResonseRedirect: Redirect to destination if found
    """
    if None in [currentPage, sourcePage]:
        print "Current or source page not specified"
        #TODO raise proper exception
        raise

    destinationURL = getDestinationURL(currentPage, sourcePage, pageKey, request.user.username)
    if not destinationURL:
        print "No url could be resolved"
        raise
    else:
        messages.add_message(request, messages.INFO,
                             "source:{0}".format(currentPage))
        return HttpResponseRedirect(destinationURL)


def getDestinationURL(currentPage, sourcePage, pageKey=None, username=None):
    """Returns a destination URL taken from the PAGE_MAP dict declared in constants.py.
    The URL is determined from the current page requesting the URL, and the source page
    that led to the current page. If there could be multiple, different destinations from
    the same currentPage and sourcePage, the pageKey is used to determine the correct one. 
    Otherwise, the default page for the current/source combo is used

    :param str currentPage: Current page name as defined in constants.py
    :param str sourcePage: Name of page that led to the current page as defined in constants.py
    :param str pageKey: Optional argument if multiple destinations exist from the same current/source
                        page combintaion, defaults to DEFAULT
    :param str username: Optional argument if the destination could be profile requiring a username
    :return str: Relative URL defined in the URL_MAP in constants.py
    """
    if not pageKey:
        pageKey = constants.DEFAULT

    currentPageMap = constants.PAGE_MAP.get(currentPage)
    if currentPageMap:
        destPageMap = currentPageMap.get(sourcePage)
        if destPageMap:
            destPageName = destPageMap.get(pageKey)
            if destPageName:
                destURL = constants.URL_MAP.get(destPageName)
                # Special case for profile
                #TODO get the username without haveing to pass the request
                if destPageName == constants.PROFILE:
                    if username:
                        destURL = destURL.format(username)
                    else:
                        print "USERNAME SHOULD HAVE BEEN PASSED"
                        destURL = "/"
                if destURL:
                    return destURL
                else:
                    print "helpers.py: getDestinationURL: no destURL found"
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
    return {"toolbarSources": {"login": constants.TOOLBAR_LOGIN,
                               "home": constants.TOOLBAR_HOME,
                               "logout": constants.TOOLBAR_LOGOUT,
                               "profile": constants.TOOLBAR_PROFILE},
            "source": source
            }


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
