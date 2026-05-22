from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import permission_classes, api_view

from rest_framework.permissions import AllowAny

from .models import Disease


# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def disease_list(request, vegetable):
    data = []

    vegatable_diseases = Disease.objects.filter(vegetable__name=vegetable)
    
    for vd in vegatable_diseases:
        data.append({
            "name":vd.name,
            "description":vd.description
        })

    return JsonResponse({
        "success":True,
        "data":data
    })


