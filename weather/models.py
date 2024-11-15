# models.py

from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Weather(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    sunlight = models.FloatField()
    wind_speed = models.FloatField()
    altitude = models.FloatField()
    soil_type = models.CharField(max_length=50)
    soil_fertility = models.CharField(max_length=50)
    soil_structure = models.CharField(max_length=50)
    soil_drainage = models.CharField(max_length=50)
    solar_radiation = models.FloatField()
    uv_radiation = models.FloatField()
    year = models.IntegerField()
    month = models.IntegerField()
    date = models.DateField(auto_now_add=True)  # Add this line to track the date of the record

    def __str__(self):
        return f"Weather record for {self.user.email} on {self.date}"
