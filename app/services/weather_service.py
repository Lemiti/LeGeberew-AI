# app/services/weather_service.py
import requests
from datetime import datetime, timedelta
import os

class WeatherService:
    def __init__(self):
        self.api_key = os.environ.get('WEATHER_API_KEY', '7fd22c8a1c924db8a63133612251811')
        self.base_url = "http://api.weatherapi.com/v1"
        
        # Ethiopian cities and their coordinates
        self.ethiopian_locations = {
            'addis_ababa': {'lat': 9.03, 'lon': 38.74},
            'bahir_dar': {'lat': 11.59, 'lon': 37.39},
            'hawassa': {'lat': 7.05, 'lon': 38.46},
            'mekele': {'lat': 13.49, 'lon': 39.47},
            'dire_dawa': {'lat': 9.60, 'lon': 41.86}
        }
    
    def get_weather_forecast(self, location='addis_ababa', days=3):
        """Get weather forecast for farming decisions"""
        try:
            if location not in self.ethiopian_locations:
                location = 'addis_ababa'
            
            coords = self.ethiopian_locations[location]
            
            # Using WeatherAPI (you registered with the key you provided)
            url = f"{self.base_url}/forecast.json"
            params = {
                'key': self.api_key,
                'q': f"{coords['lat']},{coords['lon']}",
                'days': days,
                'aqi': 'no',
                'alerts': 'yes'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self.analyze_for_farming(data, location)
            else:
                # Fallback to mock data if API fails
                return self.get_mock_weather_data(location)
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.get_mock_weather_data(location)
    
    def analyze_for_farming(self, weather_data, location):
        """Analyze weather data for farming recommendations"""
        forecast_days = weather_data.get('forecast', {}).get('forecastday', [])
        
        recommendations = []
        for day in forecast_days:
            date = day['date']
            day_data = day['day']
            astro = day['astro']
            
            # Analyze conditions
            total_precip = day_data.get('totalprecip_mm', 0)
            max_temp = day_data.get('maxtemp_c', 25)
            min_temp = day_data.get('mintemp_c', 10)
            humidity = day_data.get('avghumidity', 50)
            
            # Farming recommendations
            watering_advice = "WATERING RECOMMENDED" if total_precip < 2 else "NO WATERING NEEDED"
            if total_precip > 10:
                watering_advice = "HEAVY RAIN EXPECTED - NO WATERING"
            
            # Temperature advice
            temp_advice = []
            if max_temp > 35:
                temp_advice.append("High temperatures - consider shading for sensitive crops")
            if min_temp < 5:
                temp_advice.append("Low temperatures - protect frost-sensitive plants")
            
            # Humidity advice
            humidity_advice = []
            if humidity > 80:
                humidity_advice.append("High humidity - watch for fungal diseases")
            if humidity < 30:
                humidity_advice.append("Low humidity - plants may need more water")
            
            recommendations.append({
                'date': date,
                'location': location,
                'weather_summary': day_data.get('condition', {}).get('text', ''),
                'total_precipitation_mm': total_precip,
                'max_temperature_c': max_temp,
                'min_temperature_c': min_temp,
                'average_humidity': humidity,
                'watering_recommendation': watering_advice,
                'temperature_alerts': temp_advice,
                'humidity_advice': humidity_advice,
                'sunrise': astro.get('sunrise', ''),
                'sunset': astro.get('sunset', '')
            })
        
        return recommendations
    
    def get_mock_weather_data(self, location):
        """Provide mock weather data when API is unavailable"""
        # This ensures the app always works during development
        return [{
            'date': datetime.now().date().isoformat(),
            'location': location,
            'weather_summary': 'Partly Cloudy',
            'total_precipitation_mm': 0.5,
            'max_temperature_c': 28,
            'min_temperature_c': 12,
            'average_humidity': 65,
            'watering_recommendation': 'WATERING RECOMMENDED',
            'temperature_alerts': [],
            'humidity_advice': ['Moderate humidity - good growing conditions'],
            'sunrise': '06:30 AM',
            'sunset': '06:45 PM'
        }]