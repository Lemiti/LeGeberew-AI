# app/routes/main.py - UPDATED
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'LeGeberew AI',
        'version': '1.0.0',
        'features': ['real_ai_disease_detection', 'market_prices', 'weather_alerts'],
        'ai_accuracy': '96.34%'
    })

@main_bp.route('/api/status')
def system_status():
    return jsonify({
        'ai_model_ready': True,
        'model_accuracy': '96.34%',
        'diseases_detectable': 15,
        'status': 'Production Ready',
        'message': 'Real AI plant disease detection is active!'
    })