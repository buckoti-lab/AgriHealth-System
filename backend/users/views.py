from .serializers import RegisterSerializer, LoginSerializer,EditProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        "success":True,
        "message": "User created"
    })


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data
    refresh = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    
    data = {
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email
    }
    return Response({
         "success":True,
         "data":data
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit(request):
    serializer = EditProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        "success":True,
        "message": "User details updated"
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({
        'success': True,
        'message': 'Logged out successfully. Please delete your token on client side.'
    })
