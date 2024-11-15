from django.db import models

# Create your models here.

from users.models import CustomUser

class SimpleDroneTask(models.Model):
    TASK_TYPE_CHOICES = [
        ('spray', 'Spray'),
    ]
    
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    coordinates = models.JSONField()  # Store the coordinates in JSON
    status = models.CharField(max_length=50, default='pending')  # pending, in-progress, completed
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_type} task for {self.created_by}'
