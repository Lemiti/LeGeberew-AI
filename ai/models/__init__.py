# app/models/__init__.py
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'name': self.name,
            'location': self.location,
            'language': self.language
        }

class Crop(db.Model):
    __tablename__ = 'crops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amharic_name = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amharic_name': self.amharic_name,
            'scientific_name': self.scientific_name
        }

class MarketPrice(db.Model):
    __tablename__ = 'market_prices'
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    market_name = db.Column(db.String(200))
    price_per_kg = db.Column(db.Float)
    currency = db.Column(db.String(10), default='ETB')
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'market_name': self.market_name,
            'price_per_kg': self.price_per_kg,
            'currency': self.currency,
            'date_recorded': self.date_recorded.date().isoformat()
        }