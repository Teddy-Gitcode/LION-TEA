# weather/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Weather
from .serializers import WeatherSerializer
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

# Get the custom user model
CustomUser = get_user_model()

class WeatherFetchView(APIView):
    API_KEY = '1efdb9867ea775443643a12ae6a249e4'  # Replace with your actual API key

    def get_weather_data(self, lat, lon):
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()

    def post(self, request):
        lat = request.data.get('lat')  # Expecting latitude
        lon = request.data.get('lon')  # Expecting longitude
        user_email = request.data.get('user_email')  # Expecting user email

        if lat is None or lon is None or user_email is None:
            return Response({"error": "Latitude, longitude, and user email must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user based on provided email
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        weather_data = self.get_weather_data(lat, lon)

        if weather_data.get("cod") != 200:
            return Response({"error": "Unable to fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract relevant information
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        location = weather_data.get("name")

        # Check if a record for today already exists
        today = timezone.now().date()
        existing_record = Weather.objects.filter(user=user, date=today).first()

        if existing_record:
            # Update the existing record instead of creating a new one
            existing_record.temperature = temperature
            existing_record.humidity = humidity
            existing_record.location = location
            existing_record.save()
            serializer = WeatherSerializer(existing_record)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Save to the database
            weather_record = Weather(
                user=user,
                location=location,
                temperature=temperature,
                humidity=humidity,
                rainfall=0.0,  # Placeholder value
                sunlight=0.0,  # Placeholder value
                wind_speed=weather_data["wind"]["speed"],
                altitude=0.0,  # Placeholder value
                soil_type='unknown',
                soil_fertility='unknown',
                soil_structure='unknown',
                soil_drainage='unknown',
                solar_radiation=0.0,  # Placeholder value
                uv_radiation=0.0,  # Placeholder value
                year=today.year,
                month=today.month,
                date=today  # Set the date
            )
            weather_record.save()
            serializer = WeatherSerializer(weather_record)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# weather/views.py - Fetch user weather records

class UserWeatherRecordsView(APIView):
    def get(self, request, user_email):
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        records = Weather.objects.filter(user=user).order_by('date')  # Fetch records for the user
        serializer = WeatherSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
