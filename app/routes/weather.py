# app/routes/weather.py - FIXED
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/alert', methods=['GET'])
def get_weather_alert():
    """Get weather-based farming recommendations"""
    location = request.args.get('location', 'Addis Ababa')
    
    # Simulate weather conditions
    conditions = [
        {'rain': 15, 'temp': 22, 'humidity': 65, 'advice': 'NO WATERING NEEDED'},
        {'rain': 5, 'temp': 25, 'humidity': 45, 'advice': 'LIGHT WATERING RECOMMENDED'},
        {'rain': 0, 'temp': 28, 'humidity': 35, 'advice': 'WATERING REQUIRED'},
        {'rain': 25, 'temp': 18, 'humidity': 80, 'advice': 'HEAVY RAIN - NO WATERING'}
    ]
    
    condition = random.choice(conditions)
    
    return jsonify({
        'location': location,
        'date': datetime.now().date().isoformat(),
        'weather_alert': condition['advice'],
        'details': {
            'expected_rainfall_mm': condition['rain'],
            'average_temperature_c': condition['temp'],
            'humidity_percent': condition['humidity']
        },
        'farming_recommendations': [
            f"Rain expected: {condition['rain']}mm - {condition['advice']}",
            "Check soil moisture before watering",
            "Monitor plants for signs of stress"
        ],
        'amharic_advice': 'የዛሬው የአየር ሁኔታ ለሰብል እርባታ ተስማሚ ነው።' if condition['rain'] > 10 else 'ሰብሎችን ማጠጣት ያስፈልጋል።'
    })

@weather_bp.route('/forecast', methods=['GET'])
def get_weather_forecast():
    """Get 3-day weather forecast"""
    locations = {
        'Addis Ababa': {'lat': 9.03, 'lon': 38.74},
        'Bahir Dar': {'lat': 11.59, 'lon': 37.39},
        'Hawassa': {'lat': 7.05, 'lon': 38.46}
    }
    
    location = request.args.get('location', 'Addis Ababa')
    coords = locations.get(location, locations['Addis Ababa'])
    
    # Generate 3-day forecast
    forecast = []
    for i in range(3):
        date = datetime.now() + timedelta(days=i)
        forecast.append({
            'date': date.date().isoformat(),
            'high_temp': random.randint(20, 28),
            'low_temp': random.randint(10, 15),
            'rain_chance': random.randint(0, 80),
            'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain'])
        })
    
    return jsonify({
        'location': location,
        'coordinates': coords,
        'forecast': forecast,
        'source': 'LeGeberew Weather Service'
    })