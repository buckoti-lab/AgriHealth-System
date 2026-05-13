from django.urls import path
from .views import register, login,profile,edit,logout

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('register/', register),
    path('profile/', profile),
    path('edit/', edit),
    path('logout/', logout)
]