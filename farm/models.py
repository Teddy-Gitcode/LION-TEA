from django.db import models
from users.models import CustomUser
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


class Field(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    tea_variety = models.CharField(max_length=10, null=True,blank=True)
    alitutude = models.IntegerField(blank=True,null=True)
    soil_type = models.CharField(max_length=255,blank=True,null=True)
    soil_fertility = models.CharField(max_length=10,blank=True,null=True)
    soil_structure = models.CharField(max_length=10,blank=True,null=True)
    soil_drainage = models.CharField(max_length=10,blank=True,null=True)
    
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in hectares")
    elevation = models.IntegerField(null=True, blank=True, help_text="Elevation in meters")
    slope = models.CharField(max_length=50, help_text="Slope description, e.g., 'steep', 'gentle'")

    def __str__(self):
        return f"Field ID: {self.id}, Location: {self.location}, User Email: {self.user.email}"


class Activity(models.Model):
    FIELD_ACTIVITY_CHOICES = [
        ('harvest', 'Harvest'),
        ('planting', 'Planting'),
        ('irrigation', 'Irrigation'),
        # Add more activity types as needed
    ]
    
    field = models.ForeignKey(Field, related_name='activities', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=FIELD_ACTIVITY_CHOICES)  # Updated with choices
    harvest_type = models.CharField(
        max_length=50,
        choices=[('manual', 'Manual'), ('machine', 'Machine')],
        blank=True,
        null=True
    )
    num_workers = models.IntegerField(blank=True, null=True)  # Auto-calculated
    expected_yield_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Auto-calculated
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Auto-calculated
    last_harvest_date = models.DateTimeField(null=True, blank=True)
    next_harvest_date = models.DateTimeField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Activity: {self.activity_type} on Field ID: {self.field.id}, User Email: {self.field.user.email}"

    def save(self, *args, **kwargs):
        # Choose harvest type based on slope and elevation
        if not self.harvest_type:
            self.harvest_type = self.choose_harvest_type()
        # Calculate other fields
        self.num_workers = self.calculate_num_workers()
        self.expected_yield_kg = self.calculate_expected_yield()
        self.cost_estimate = self.calculate_cost()
        self.next_harvest_date = self.get_next_harvest_date()
        super().save(*args, **kwargs)

    def choose_harvest_type(self):
        # Prefer machine if the slope is not steep and the elevation is not very high
        if self.field.slope.lower() != 'steep' and self.field.elevation < 1000:
            return 'machine'
        return 'manual'

    def calculate_num_workers(self):
        # Example logic based on farm size and harvesting method
        field_size = self.field.size
        if self.harvest_type == 'manual':
            # Manual harvest requires more workers (around 10 workers per hectare, adjust as necessary)
            return int(field_size * 10)  # 10 workers per hectare
        elif self.harvest_type == 'machine':
            # Machine harvest requires fewer workers (around 2 workers per hectare)
            return max(1, int(field_size * 2))  # At least 1 worker for machine
        return 0

    def calculate_expected_yield(self):
        # Elevation affects yield, but also soil type and weather play a big role
        elevation_factor = Decimal(100) - (Decimal(self.field.elevation) * Decimal(0.05)) if self.field.elevation else Decimal(0)
        soil_quality_factor = Decimal(1.2)  # Example: Soil quality impacts yield by 20%
        return round(self.field.size * elevation_factor * soil_quality_factor, 2)

    def calculate_cost(self):
        # Calculate cost based on the harvesting method and number of workers
        labor_cost_per_worker = 100 if self.harvest_type == 'manual' else 50
        machine_cost_per_hectare = 500 if self.harvest_type == 'machine' else 0
        # Cost formula includes both worker and machine cost (machine cost is per hectare)
        return (self.num_workers * labor_cost_per_worker) + (machine_cost_per_hectare * self.field.size)

    def get_next_harvest_date(self):
        # If self.date is None, set it to the current date and time
        if not self.date:
            self.date = timezone.now()  # Assuming you're using Django's timezone functionality
        # Next harvest is approximately 14 days from the current date
        return self.date + timedelta(days=14)


class Alert(models.Model):
    field = models.ForeignKey('farm.Field', on_delete=models.CASCADE, related_name='alert')  # For Alert


    alert_type = models.CharField(max_length=50)  # e.g., Pest Outbreak, Low Soil Moisture
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert: {self.alert_type} for Field ID: {self.field.id}, User Email: {self.field.user.email}"
