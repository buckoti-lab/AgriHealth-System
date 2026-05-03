from django.urls import path
from .views import register, login, logout, protected_view

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('',protected_view),
    path('token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('register/', register),
    # path('login/', login),
    path('logout/', logout)
]