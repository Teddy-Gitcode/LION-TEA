# disease_detection/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company

@api_view(['GET'])
def best_company(request):
    best_company = Company.objects.order_by('-price_per_kg', '-quality_acceptance').first()
    
    if best_company:
        return Response({
            'name': best_company.name,
            'price_per_kg': best_company.price_per_kg,
            'quality_acceptance': best_company.quality_acceptance,
            'payment_terms': best_company.payment_terms,
            'pickup_schedule': best_company.pickup_schedule
        })
    else:
        return Response({'error': 'No company data available.'}, status=404)
