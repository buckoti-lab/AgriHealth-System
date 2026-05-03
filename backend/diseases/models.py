from django.db import models
from crops.models import Vegetable as V

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    vegetable = models.ForeignKey(V, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name