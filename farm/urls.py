from django.urls import path
from .views import (
    ActivityDeleteView, FieldCreateView, FieldListView, FieldDeleteView, 
    ActivityCreateView, ActivityListView, AlertCreateView, AlertListView,
)

urlpatterns = [
    # Field URLs
    path('field/create/', FieldCreateView.as_view(), name='create_field'),
    path('field/list/', FieldListView.as_view(), name='list_fields'),
    path('field/delete/<int:pk>/', FieldDeleteView.as_view(), name='delete_field'),  # Correct URL for deleting field

    # Activity URLs
    path('field/activity/create/', ActivityCreateView.as_view(), name='create_activity'),
    path('field/activity/list/<int:field_id>/', ActivityListView.as_view(), name='list_activity'),
    
    path('farms/field/activity/delete/<int:field_id>/<int:activity_id>/', ActivityDeleteView.as_view(), name='activity-delete'),



# Added field_id as part of URL

    # Alert URLs
    path('alert/create/', AlertCreateView.as_view(), name='create_alert'),
    path('alert/list/<int:field_id>/', AlertListView.as_view(), name='list_field_alerts'),  # Changed to int for consistency with field_id

    # Add paths for produce views if required
    # path('produce/create/', ProduceCreateView.as_view(), name='create_produce'),
    # path('produce/list/', ProduceListView.as_view(), name='list_produce'),
]
