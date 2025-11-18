# app/services/market_service.py
import requests
import pandas as pd
from datetime import datetime, timedelta
from app.models import MarketPrice, Crop, db
import os

class MarketPriceService:
    def __init__(self):
        self.ethiopian_markets = [
            "Addis Mercato", "Shola Market", "Merkato", 
            "Bahir Dar", "Hawassa", "Mekele", "Dire Dawa"
        ]
    
    def update_market_prices(self):
        """Update market prices from various sources"""
        try:
            # This would integrate with real Ethiopian market APIs
            # For now, we'll simulate realistic price data
            
            crops = Crop.query.all()
            
            for crop in crops:
                for market in self.ethiopian_markets:
                    # Simulate price variation
                    base_prices = {
                        'Teff': 45.0,
                        'Maize': 18.0,
                        'Wheat': 22.0,
                        'Barley': 20.0,
                        'Sorghum': 16.0,
                        'Coffee': 120.0
                    }
                    
                    base_price = base_prices.get(crop.name, 25.0)
                    # Add some random variation
                    import random
                    price_variation = random.uniform(-5, 5)
                    current_price = base_price + price_variation
                    
                    # Create or update price record
                    price_record = MarketPrice(
                        crop_id=crop.id,
                        market_name=market,
                        price_per_kg=round(current_price, 2),
                        source='LeGeberew AI Simulation'
                    )
                    
                    db.session.add(price_record)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error updating market prices: {e}")
            return False
    
    def get_current_prices(self, crop_name=None, market=None):
        """Get current market prices with filtering"""
        try:
            query = MarketPrice.query.join(Crop)
            
            if crop_name:
                query = query.filter(Crop.name == crop_name)
            if market:
                query = query.filter(MarketPrice.market_name == market)
            
            # Get latest prices (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            prices = query.filter(MarketPrice.date_recorded >= week_ago)\
                .order_by(MarketPrice.date_recorded.desc())\
                .all()
            
            return [price.to_dict() for price in prices]
            
        except Exception as e:
            print(f"Error getting prices: {e}")
            return []
    
    def get_price_trends(self, crop_name, days=30):
        """Get price trends for a specific crop"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            prices = MarketPrice.query.join(Crop)\
                .filter(Crop.name == crop_name)\
                .filter(MarketPrice.date_recorded >= start_date)\
                .order_by(MarketPrice.date_recorded)\
                .all()
            
            trend_data = []
            for price in prices:
                trend_data.append({
                    'date': price.date_recorded.date().isoformat(),
                    'price': price.price_per_kg,
                    'market': price.market_name
                })
            
            return trend_data
            
        except Exception as e:
            print(f"Error getting price trends: {e}")
            return []