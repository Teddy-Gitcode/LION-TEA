import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Function to fetch weather data for the last 3 months
def fetch_weather_data(lat, lon):
    api_key = '1efdb9867ea775443643a12ae6a249e4'  # Replace with your actual API key
    url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"
    weather_data = []

    for i in range(90):  # Fetch data for the last 90 days
        date = (datetime.now() - timedelta(days=i)).timestamp()
        params = {
            'lat': lat,
            'lon': lon,
            'dt': int(date),
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data.append(data['current'])  # Current day weather

    # Calculate averages for temp, humidity, rainfall
    avg_temp = sum(d['temp'] for d in weather_data) / len(weather_data)
    avg_humidity = sum(d['humidity'] for d in weather_data) / len(weather_data)
    avg_rainfall = sum(d['rain'] for d in weather_data if 'rain' in d) / len([d for d in weather_data if 'rain' in d])

    return {
        'avg_temp': avg_temp,
        'avg_humidity': avg_humidity,
        'avg_rainfall': avg_rainfall
    }

# Function to scrape Germini data for the predicted disease
def scrape_germini_data(disease_name):
    url = f"https://germini.com/diseases/{disease_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        additional_info = soup.find('div', {'class': 'disease-info'}).text
        return additional_info
    return None

# Function to generate content using the Google Generative Language API (Gemini API)
def generate_gemini_content(disease_name):
    api_key = 'AIzaSyCK-BXQ8z5v80I-csF0DiRl34GwJuCAkYE'  # Replace with your actual Gemini API key
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'
    
    # The prompt for generating the content
    prompt = f"Explain the disease {disease_name} in tea plants"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    # Send the POST request to Google Gemini API
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        # Parse the response to get the generated content
        response_data = response.json()
        generated_content = response_data['contents'][0]['parts'][0]['text']
        return generated_content
    else:
        # Handle errors
        return f"Error: Unable to generate content, status code {response.status_code}"
