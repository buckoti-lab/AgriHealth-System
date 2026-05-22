from django.urls import path
from .views import disease_list

urlpatterns = [
    path('list/<str:vegetable>', disease_list),
]