from django.urls import path
from . import views


urlpatterns = [
    path('', views.endpoints),
    path('farmers/', views.farmer_list),
    
    path('farmers/<str:username>/', views.farmer_detail),
]
