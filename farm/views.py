from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import CustomUser
from .models import Field, Activity, Alert
from .serializers import FieldSerializer, ActivitySerializer, AlertSerializer
from django.core.exceptions import ObjectDoesNotExist

# Field Views
class FieldCreateView(generics.CreateAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_email = self.request.data.get('user_email')
        try:
            user = CustomUser.objects.get(email=user_email)  # Get user by email
            serializer.save(user=user)  # Associate field with user
        except ObjectDoesNotExist:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

class FieldListView(generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_email = self.request.query_params.get('user_email')
        if user_email:
            try:
                user = CustomUser.objects.get(email=user_email)
                return Field.objects.filter(user=user)  # Filter fields by user
            except ObjectDoesNotExist:
                return Field.objects.none()
        else:
            return Field.objects.none()

class FieldDeleteView(generics.DestroyAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Field.objects.filter(user=self.request.user)

# Activity Views
class ActivityCreateView(generics.CreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        return Activity.objects.filter(field__id=field_id, field__user=self.request.user)

# Alert Views
class AlertCreateView(generics.CreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        resolved = self.request.query_params.get('resolved', 'false').lower() == 'true'
        return Alert.objects.filter(field__id=field_id, resolved=resolved, field__user=self.request.user)
