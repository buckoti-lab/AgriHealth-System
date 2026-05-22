from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

from .models import Vegetable

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def vegetable_list(request):
    data = []
    vegetables = Vegetable.objects.all()
    for v in vegetables:
        data.append({
            "crop":v.name,
            "description":v.description
        })

    return JsonResponse({
        "success":True,
        "data":data
    })
