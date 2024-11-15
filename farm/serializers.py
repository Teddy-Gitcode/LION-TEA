from rest_framework import serializers
from .models import Field, Activity, Alert

class FieldSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')  # Assuming you want to show the user's email

    class Meta:
        model = Field
        fields = [
            'id', 'user','location', 'tea_variety','alitutude', 'soil_type','soil_fertility','soil_structure','soil_drainage ','size', 'slope', 'elevation'
        ]


class ActivitySerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), write_only=True)
    field_info = FieldSerializer(source='field', read_only=True)  # Nested field info

    class Meta:
        model = Activity
        fields = [
            'id', 'field', 'field_info', 'activity_type', 'harvest_type', 
            'num_workers', 'expected_yield_kg', 'cost_estimate', 
            'last_harvest_date', 'next_harvest_date', 'details', 'date'
        ]
        read_only_fields = ['num_workers', 'expected_yield_kg', 'cost_estimate', 'next_harvest_date']


class AlertSerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), write_only=True)
    field_info = FieldSerializer(source='field', read_only=True)  # Nested field info

    class Meta:
        model = Alert
        fields = [
            'id', 'field', 'field_info', 'alert_type', 'description', 
            'date', 'resolved'
        ]
