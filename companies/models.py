# disease_detection/models.py

from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    quality_acceptance = models.FloatField()  # Assuming a rating from 0 to 100
    payment_terms = models.CharField(max_length=255)
    pickup_schedule = models.CharField(max_length=255)

    def __str__(self):
        return self.name
