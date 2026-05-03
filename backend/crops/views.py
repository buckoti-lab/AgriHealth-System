from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse

# Create your views here.

def home(request):
    data = {
        "message":"Crops home"
    }
    # return JsonResponse(data)
    return HttpResponse("<h2>Crops home</h2>")
