from rest_framework import serializers
from .models import SimpleDroneTask

class SimpleDroneTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleDroneTask
        fields = ['id', 'task_type', 'coordinates', 'status', 'created_at']
