from django.db import models

class Vegetable(models.Model):
    name = models.CharField(max_length=50)  # You might want a slightly larger max_length
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name