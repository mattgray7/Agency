from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

def call(request):
    if request.POST and request.POST.get("method"):
        return JsonResponse(globals().get(request.POST.get("method"))(request))
    else:
        print "ajax.call: Request is not valid"

