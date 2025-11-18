# run.py - UPDATED (no flask_migrate)
from app import create_app, db
from app.models import User, Crop, MarketPrice
import os

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Add sample Ethiopian crops
        crops = [
            Crop(name='Teff', amharic_name='ጤፍ', scientific_name='Eragrostis tef'),
            Crop(name='Maize', amharic_name='ገብስ', scientific_name='Zea mays'),
            Crop(name='Wheat', amharic_name='ስር', scientific_name='Triticum aestivum'),
            Crop(name='Barley', amharic_name='ገብስ ስንዴ', scientific_name='Hordeum vulgare'),
            Crop(name='Sorghum', amharic_name='ማሸጋ', scientific_name='Sorghum bicolor'),
            Crop(name='Coffee', amharic_name='ቡና', scientific_name='Coffea arabica')
        ]
        
        for crop in crops:
            existing = Crop.query.filter_by(name=crop.name).first()
            if not existing:
                db.session.add(crop)
                print(f"✅ Added {crop.name}")
        
        db.session.commit()
        print("🎉 Database initialized with Ethiopian crops!")

@app.cli.command("create-upload-dir")
def create_upload_dir():
    """Create upload directory for plant images"""
    os.makedirs('static/uploads', exist_ok=True)
    print("✅ Created upload directory: static/uploads/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)