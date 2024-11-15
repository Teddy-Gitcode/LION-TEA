from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SignupSerializer, LoginSerializer, MyTokenObtainPairSerializer

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Signup View
@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response({
            "message": "Login successful",
            "user_id": serializer.validated_data['user_id'],  # Include user ID in response
            "access": serializer.validated_data['access'],    # Include access token
            "refresh": serializer.validated_data['refresh'],  # Include refresh token
            "name": serializer.validated_data['name'],        # Include user name in response
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/signup/',
        '/api/login/',
        '/api/token/',
        '/api/token/refresh/',
    ]
    return Response(routes)
