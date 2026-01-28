import requests
from django.conf import settings

def get_ambient_temperature(lat, lon):
    """
    Fetches the current ambient temperature from OpenWeatherMap.

    Args:
        lat (float): The latitude.
        lon (float): The longitude.

    Returns:
        float: The current ambient temperature in Celsius.
    """
    api_key = getattr(settings, "OPENWEATHERMAP_API_KEY", None)
    if not api_key:
        # Return a default value for testing if no API key is set
        return 25.0 

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['main']['temp']
    except requests.exceptions.RequestException as e:
        # Log the error and return a default value
        print(f"Could not fetch weather data: {e}")
        return 25.0 # Default to 25C on failure
