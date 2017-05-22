from django.http import JsonResponse

import post
import models


def followPost(request, postID):
	if post.isFollowingPost(postID, request.user.username):
		success = post.unfollowPost(postID=postID, username=request.user.username)
	else:
		success = post.followPost(postID=postID, username=request.user.username)
	return JsonResponse({"success": success})


def getPostFollowingBool(request):
	return JsonResponse({"following": isFollowingPost(request.POST.get("postID"),
													  username=request.user.username)})


