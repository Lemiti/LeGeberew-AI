# app/routes/market.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random

market_bp = Blueprint('market', __name__)

# Ethiopian crops and typical price ranges (in ETB per kg)
CROP_PRICES = {
    'Teff': {'min': 40, 'max': 50},
    'Maize': {'min': 15, 'max': 20},
    'Wheat': {'min': 20, 'max': 25},
    'Barley': {'min': 18, 'max': 22},
    'Sorghum': {'min': 14, 'max': 18},
    'Coffee': {'min': 100, 'max': 130}
}

ETHIOPIAN_MARKETS = [
    'Addis Mercato', 'Shola Market', 'Merkato', 
    'Bahir Dar', 'Hawassa', 'Mekele', 'Dire Dawa'
]

@market_bp.route('/prices', methods=['GET'])
def get_market_prices():
    """Get current market prices for Ethiopian crops"""
    crop = request.args.get('crop', 'Teff')
    
    if crop not in CROP_PRICES:
        return jsonify({'error': 'Crop not found'}), 404
    
    price_range = CROP_PRICES[crop]
    
    # Generate realistic prices with some variation
    prices = []
    for market in ETHIOPIAN_MARKETS:
        base_price = random.uniform(price_range['min'], price_range['max'])
        # Add some market-specific variation
        variation = random.uniform(-3, 3)
        final_price = round(base_price + variation, 2)
        
        prices.append({
            'market': market,
            'price': final_price,
            'currency': 'ETB',
            'unit': 'per kg',
            'last_updated': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat()
        })
    
    # Sort by price (lowest first)
    prices.sort(key=lambda x: x['price'])
    
    return jsonify({
        'crop': crop,
        'prices': prices,
        'average_price': round(sum(p['price'] for p in prices) / len(prices), 2),
        'best_price': prices[0]['price'],
        'best_market': prices[0]['market']
    })

@market_bp.route('/crops')
def get_available_crops():
    """List all available crops"""
    return jsonify({
        'crops': list(CROP_PRICES.keys()),
        'count': len(CROP_PRICES)
    })