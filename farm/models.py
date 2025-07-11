from django.db import models # type: ignore
from users.models import CustomUser
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone # type: ignore
from django.db.models import Max

class Field(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fields')
    user_field_id = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    tea_variety = models.CharField(max_length=50, null=True,blank=True)
    alitutude = models.IntegerField(blank=True,null=True)
    soil_type = models.CharField(max_length=255,blank=True,null=True)
    soil_fertility = models.CharField(max_length=50,blank=True,null=True)
    soil_structure = models.CharField(max_length=50,blank=True,null=True)
    soil_drainage = models.CharField(max_length=50,blank=True,null=True)
    
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in hectares")
    elevation = models.IntegerField(null=True, blank=True, help_text="Elevation in meters")
    slope = models.CharField(max_length=50, help_text="Slope description, e.g., 'steep', 'gentle'")

    def save(self, *args, **kwargs):
        if not self.pk:
            max_id = self.__class__.objects.filter(user=self.user).aggregate(Max('user_field_id'))['user_field_id__max']
            self.user_field_id = 1 if not max_id else max_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        user_email = getattr(self.user, 'email', 'unknown')
        return f"Field #{self.user_field_id} (User: {user_email}) - Location: {self.location}"



from datetime import timedelta
from decimal import Decimal


from datetime import timedelta
from decimal import Decimal

class Activity(models.Model):
    FIELD_ACTIVITY_CHOICES = [
        ('harvest', 'Harvest'),
        ('pruning', 'Pruning'),
        ('irrigation', 'Irrigation'),
        ('fertilizing', 'Fertilizing'),
    ]

    field = models.ForeignKey(Field, related_name='activities', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=FIELD_ACTIVITY_CHOICES)
    harvest_type = models.CharField(max_length=50, blank=True, null=True)
    num_workers = models.IntegerField(blank=True, null=True)
    expected_yield_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    last_harvest_date = models.DateTimeField(null=True, blank=True)
    next_harvest_date = models.DateTimeField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def calculate_num_workers(self):
        field_size = self.field.size
        if self.activity_type == 'harvest':
            return max(1, int(field_size * 15))  # 15 workers per hectare for tea harvesting
        elif self.activity_type == 'pruning':
            return max(1, int(field_size * 10))  # 10 workers per hectare
        elif self.activity_type == 'irrigation':
            return max(1, int(field_size * 5))  # 5 workers per hectare
        elif self.activity_type == 'fertilizing':
            return max(1, int(field_size * 8))  # 8 workers per hectare
        return 0

    def calculate_expected_yield(self):
        if self.activity_type != 'harvest':
            return Decimal(0)
        elevation_factor = Decimal(1.0 - (self.field.elevation * 0.0001))  # Decrease by 0.01% per meter elevation
        yield_per_hectare = Decimal(500)  # Average yield in kg per hectare
        return round(self.field.size * yield_per_hectare * elevation_factor, 2)

    def calculate_cost(self):
        labor_cost_per_worker = Decimal(150)  # Average daily cost per worker
        field_size = self.field.size
        if self.activity_type == 'harvest':
            return round(self.num_workers * labor_cost_per_worker, 2)
        elif self.activity_type in ['pruning', 'irrigation', 'fertilizing']:
            activity_cost = Decimal(300 if self.activity_type == 'fertilizing' else 200) * field_size
            return round((self.num_workers * labor_cost_per_worker) + activity_cost, 2)
        return Decimal(0)

    def get_next_harvest_date(self):
        """
        Calculate the next harvest date based on a fixed interval.
        """
        harvest_interval = 14  # Default interval for tea harvesting in days
        base_date = self.date or timezone.now()
        return base_date + timedelta(days=harvest_interval)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()

        if self.activity_type == 'harvest':
            self.num_workers = self.calculate_num_workers()
            self.expected_yield_kg = self.calculate_expected_yield()
            self.next_harvest_date = self.get_next_harvest_date()
        else:
            self.num_workers = self.calculate_num_workers()
            self.expected_yield_kg = Decimal(0)
            self.next_harvest_date = None

        self.cost_estimate = self.calculate_cost()
        super().save(*args, **kwargs)







class Alert(models.Model):
    field = models.ForeignKey('farm.Field', on_delete=models.CASCADE, related_name='alert')  # For Alert


    alert_type = models.CharField(max_length=50)  # e.g., Pest Outbreak, Low Soil Moisture
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert: {self.alert_type} for Field ID: {self.field.id}, User Email: {self.field.user.email}"
