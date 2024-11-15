from django.urls import path
from .views import best_company

urlpatterns = [
    path('best/', best_company, name='best-company'),
]
