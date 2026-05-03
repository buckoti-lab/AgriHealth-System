from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from datetime import datetime
import os


def upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"uploads/{instance.uploaded_by.username}_{timestamp}{ext}"


class Image(models.Model):
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    image_file = models.ImageField(upload_to=upload_path) 

    def __str__(self):
        return f"{self.name} by {self.uploaded_by.username}"