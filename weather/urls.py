# weather/urls.py
from django.urls import path
from .views import WeatherFetchView, UserWeatherRecordsView

urlpatterns = [
    path('fetch-weather/', WeatherFetchView.as_view(), name='fetch_weather'),
    path('user_weather_records/<str:user_email>/', UserWeatherRecordsView.as_view(), name='user_weather_records'),
]
