from datetime import datetime
from rest_framework import serializers
from .models import Field, Activity, Alert

class FieldSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')  # Assuming you want to show the user's email

    class Meta:
        model = Field
        fields = [
            'id', 'user','location', 'tea_variety','alitutude', 'soil_type','soil_fertility','soil_structure','soil_drainage','size', 'slope', 'elevation'
        ]


class ActivitySerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), write_only=True)
    field_info = FieldSerializer(source='field', read_only=True)  # Nested field info
    
    # Include any dynamic or calculated fields if needed
    num_workers = serializers.IntegerField(read_only=True)
    expected_yield_kg = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cost_estimate = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    next_harvest_date = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'field', 'field_info', 'activity_type', 'harvest_type', 
            'num_workers', 'expected_yield_kg', 'cost_estimate', 
            'last_harvest_date', 'next_harvest_date', 'details', 'date'
        ]
        read_only_fields = ['num_workers', 'expected_yield_kg', 'cost_estimate', 'next_harvest_date']

    def validate(self, attrs):
        """
        Optionally, validate input data if needed.
        e.g., check if certain fields are appropriate based on activity type.
        """
        # Normalize activity_type to lowercase
        activity_type = attrs.get('activity_type')
        if activity_type:
            activity_type = activity_type.lower()  # Convert to lowercase for consistency
            if activity_type not in ['harvest', 'planting', 'irrigation']:
                raise serializers.ValidationError("Invalid activity type.")
            attrs['activity_type'] = activity_type  # Update the attribute with normalized value
        
        # Normalize harvest_type to lowercase
        harvest_type = attrs.get('harvest_type')
        if harvest_type:
            harvest_type = harvest_type.lower()  # Normalize to lowercase
            if harvest_type not in ['manual', 'machine']:
                raise serializers.ValidationError("Invalid harvest type.")
            attrs['harvest_type'] = harvest_type  # Update the attribute with normalized value
        
        # Ensure 'last_harvest_date' is in the right format and is a valid date
        last_harvest_date = attrs.get('last_harvest_date')
        if last_harvest_date:
            if not isinstance(last_harvest_date, datetime):
                raise serializers.ValidationError("Invalid date format for 'last_harvest_date'.")
        
        # Ensure 'field' is provided
        if not attrs.get('field'):
            raise serializers.ValidationError("Field is required.")
        
        # Ensure 'harvest_type' is provided
        if not attrs.get('harvest_type'):
            raise serializers.ValidationError("Harvest type is required.")
        
        return attrs



class AlertSerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), write_only=True)
    field_info = FieldSerializer(source='field', read_only=True)  # Nested field info

    class Meta:
        model = Alert
        fields = [
            'id', 'field', 'field_info', 'alert_type', 'description', 
            'date', 'resolved'
        ]
