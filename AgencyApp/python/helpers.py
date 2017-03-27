from django.contrib import messages


def getMessageFromKey(request, key):
    """Returns the value of a key included in a message object.

    :param WSGIRequest request: The request to get the message from
    :param str key: The key to return the value for
    :return: The value of the key, None if key doesn't exist
    """
    messagesList = messages.get_messages(request)
    for message in messagesList:
    	# TODO convert unicode messages.messages to dict
    	"""if key in message.message.keys():
    		print "Observed message:{0}".format(message.message)
    		return message.message[key]"""
    	return message.message
    return None
    """for message in messages:
        #TODO use an enum
        if message.message == "login_success":
            status = message.message
            break
        elif message.message == "create_success":
            status = message.message
            break"""


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
