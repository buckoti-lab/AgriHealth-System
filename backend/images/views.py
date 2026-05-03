from django.shortcuts import render,HttpResponse
from django.http.response import JsonResponse

# Create your views here.

def home(request):
    data = {
        "message":"Images home"
    }
    return JsonResponse(data)
    # return HttpResponse("done")
