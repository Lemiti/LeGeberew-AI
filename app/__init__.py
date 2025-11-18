# app/__init__.py - UPDATED (no flask_migrate)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.disease import disease_bp
    from app.routes.market import market_bp
    from app.routes.weather import weather_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(disease_bp, url_prefix='/api/v1/disease')
    app.register_blueprint(market_bp, url_prefix='/api/v1/market')
    app.register_blueprint(weather_bp, url_prefix='/api/v1/weather')
    
    return app