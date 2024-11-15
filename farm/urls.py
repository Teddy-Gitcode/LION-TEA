# farm/urls.py

from django.urls import path
from .views import FieldCreateView, FieldListView, FieldDeleteView, ActivityCreateView, AlertCreateView, AlertListView

urlpatterns = [
    # Field URLs
    path('field/create/', FieldCreateView.as_view(), name='create_field'),
    path('field/list/', FieldListView.as_view(), name='list_fields'),
    path('field/delete/<int:id>/', FieldDeleteView.as_view(), name='delete_field'),
    
    # Activity URLs
    path('activity/create/', ActivityCreateView.as_view(), name='create_activity'),

    # Alert URLs
    path('alert/create/', AlertCreateView.as_view(), name='create_alert'),
    path('alert/list/<str:field_id>/', AlertListView.as_view(), name='list_field_alerts'),
]
