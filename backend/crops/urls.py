from django.urls import path
from .views import vegetable_list

urlpatterns = [
    path('list/', vegetable_list),
]