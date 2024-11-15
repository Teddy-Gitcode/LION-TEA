from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import CustomUser
from .models import Field, Activity, Alert
from .serializers import FieldSerializer, ActivitySerializer, AlertSerializer

# Field Views
class FieldCreateView(generics.CreateAPIView):
    serializer_class = FieldSerializer

    def perform_create(self, serializer):
        user_email = self.request.data.get('user_email')
        user = CustomUser.objects.get(email=user_email)  # Get user by email
        serializer.save(user=user)  # Associate field with user
 # Assign the user automatically

class FieldListView(generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Field.objects.filter(user=self.request.user)  # Return only fields owned by the user

class FieldDeleteView(generics.DestroyAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure that users can only delete their own fields
        return Field.objects.filter(user=self.request.user)

# Activity Views
class ActivityCreateView(generics.CreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()  # Ensure the user is associated in the ActivitySerializer

class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        # Ensure the user can only access activities for their own fields
        return Activity.objects.filter(field__field_id=field_id, field__user=self.request.user)

# Alert Views
class AlertCreateView(generics.CreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()  # Ensure the user is associated in the AlertSerializer

class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        resolved = self.request.query_params.get('resolved', 'false').lower() == 'true'
        # Ensure the user can only access alerts for their own fields
        return Alert.objects.filter(field__field_id=field_id, resolved=resolved, field__user=self.request.user)

#ADD PRODUCE VIEW
