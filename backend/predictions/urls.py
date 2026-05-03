from django.urls import path
from .views import predict,history,recent,delete

urlpatterns = [
    path('predict/',predict),
    path('predictions/history', history),
    path('predictions/recent', recent),
    path('predictions/<int:pk>/', delete),
]