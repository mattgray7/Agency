from django.http import JsonResponse

import post
import models
import constants


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
