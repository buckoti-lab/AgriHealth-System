from django.db import models
from django.contrib.auth import get_user_model
from images.models import Image
from crops.models import Vegetable
from diseases.models import Disease

User = get_user_model()

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)

    crop_confidence = models.FloatField()
    disease_confidence = models.FloatField()
    crop_energy = models.FloatField(null=True)
    disease_energy = models.FloatField(null=True)
    crop_m_distance = models.FloatField(null=True)
    disease_m_distance = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)