from datetime import datetime
from rest_framework import serializers
from .models import Field, Activity, Alert
from django.utils.dateparse import parse_datetime

class FieldSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')  # Assuming you want to show the user's email

    class Meta:
        model = Field
        fields = [
            'id',  # global id
            'user_field_id',  # per-user id
            'user', 'location', 'tea_variety','alitutude', 'soil_type','soil_fertility','soil_structure','soil_drainage','size', 'slope', 'elevation'
        ]


class ActivitySerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), write_only=True)
    field_info = FieldSerializer(source='field', read_only=True)
    
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
        activity_type = attrs.get('activity_type', '').lower()
        harvest_type = attrs.get('harvest_type', '').lower()
        
        if activity_type and activity_type not in ['harvest', 'planting', 'irrigation','fertilizing']:
            raise serializers.ValidationError({"activity_type": "Invalid activity type."})
        attrs['activity_type'] = activity_type

        if harvest_type and harvest_type not in ['manual', 'machine']:
            raise serializers.ValidationError({"harvest_type": "Invalid harvest type."})
        attrs['harvest_type'] = harvest_type

        last_harvest_date = attrs.get('last_harvest_date')
        if last_harvest_date:
            if isinstance(last_harvest_date, str):
                parsed_date = parse_datetime(last_harvest_date)
                if not parsed_date:
                    raise serializers.ValidationError({"last_harvest_date": "Invalid date format."})
                attrs['last_harvest_date'] = parsed_date

        if not attrs.get('field'):
            raise serializers.ValidationError({"field": "Field is required."})

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
