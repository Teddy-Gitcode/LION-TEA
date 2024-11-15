from rest_framework import serializers 
from .models import Company
class CompanySerializer(serializers.ModelSerializer): 
    class Meta: model = Company 
    fields = ['id', 'name', 'price_per_kg', 'quality_acceptance', 'payment_terms', 'pickup_schedule', 'location']
