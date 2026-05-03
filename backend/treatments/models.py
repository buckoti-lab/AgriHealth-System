from django.db import models
from diseases.models import Disease

class Treatment(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    solution = models.TextField()  
    prevention = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.disease.name} - {self.solution[:30]}..."