# ai/services/real_disease_predictor.py
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import os
from datetime import datetime

class RealDiseasePredictor:
    def __init__(self):
        self.model = None
        self.class_names = {}
        self.idx_to_class = {}
        self.load_model()
        
    def load_model(self):
        """Load the trained model and class names"""
        try:
            self.model = tf.keras.models.load_model('ai/models/final_plant_model.h5')
            with open('ai/models/class_names.json', 'r') as f:
                self.class_names = json.load(f)
            self.idx_to_class = {v: k for k, v in self.class_names.items()}
            print("✅ AI Model loaded successfully!")
            print(f"📊 Model can identify {len(self.class_names)} plant diseases")
            print("🎯 Accuracy: 96.34% (from training)")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def predict_disease(self, image_path):
        """Predict plant disease from image using real AI"""
        if self.model is None:
            return {
                'success': False,
                'error': 'Model not loaded',
                'timestamp': datetime.utcnow().isoformat()
            }
        
        try:
            # Load and preprocess image
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            predicted_class = self.idx_to_class[predicted_class_idx]
            
            # Get treatment advice
            treatment_info = self.get_treatment_advice(predicted_class)
            
            return {
                'success': True,
                'disease': predicted_class,
                'confidence': float(confidence),
                'treatment_advice': treatment_info['treatment'],
                'amharic_advice': treatment_info['amharic'],
                'prevention_tips': treatment_info['prevention'],
                'organic_options': treatment_info['organic'],
                'timestamp': datetime.utcnow().isoformat(),
                'model_accuracy': '96.34%'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def get_treatment_advice(self, disease_name):
        """Get comprehensive treatment advice for detected disease"""
        treatment_db = {
            'Tomato_Early_blight': {
                'treatment': 'Apply copper-based fungicide every 7-10 days. Remove and destroy infected leaves. Improve air circulation.',
                'amharic': 'ከሚያስከትሉ ንጥረ ነገሮች ጋር የተለቀ ማር በየ 7-10 ቀናት ይበጁ። የተበሳጩ ቅጠሎችን ያስወግዱ። የአየር ማስተላለፍን ያሻሽሉ።',
                'prevention': [
                    'Rotate crops yearly with non-solanaceous plants',
                    'Ensure good air circulation between plants',
                    'Water at base of plant, avoid wetting leaves',
                    'Remove plant debris at end of season'
                ],
                'organic': 'Use neem oil spray or baking soda solution (1 tbsp baking soda + 1 tsp horticultural oil + 1 gallon water)'
            },
            'Tomato_Late_blight': {
                'treatment': 'Apply fungicides containing chlorothalonil or mancozeb immediately. Remove severely infected plants.',
                'amharic': 'ወዲያውኑ ክሎሮታሎኒል ወይም ማንኮዜብ የያዙ ንጥረ ነገሮችን ይበጁ። ከፍተኛ የተበሳጩ ተክሎችን ያስወግዱ።',
                'prevention': [
                    'Use resistant tomato varieties',
                    'Avoid overhead watering',
                    'Space plants properly for air circulation',
                    'Apply preventative fungicides in humid weather'
                ],
                'organic': 'Copper-based fungicides applied every 7-10 days during favorable disease conditions'
            },
            'Tomato_Bacterial_spot': {
                'treatment': 'Apply copper-based bactericide. Remove severely infected plants to prevent spread.',
                'amharic': 'ከሚያስከትሉ ንጥረ ነገሮች ጋር የተለቀ ባክተሪያ ይበጁ። ለማራገፍ ከፍተኛ የተበሳጩ ተክሎችን ያስወግዱ።',
                'prevention': [
                    'Use disease-free seeds and transplants',
                    'Avoid working with plants when wet',
                    'Sterilize gardening tools regularly',
                    'Practice crop rotation'
                ],
                'organic': 'Copper fungicide sprays and plant-based bactericides'
            },
            'Potato___Early_blight': {
                'treatment': 'Apply fungicides containing chlorothalonil or azoxystrobin. Remove infected leaves.',
                'amharic': 'ክሎሮታሎኒል ወይም አዞክሲስትሮቢን የያዙ ንጥረ ነገሮችን ይበጁ። የተበሳጩ ቅጠሎችን ያስወግዱ።',
                'prevention': [
                    'Practice 3-year crop rotation',
                    'Ensure proper plant spacing',
                    'Water in morning to allow leaves to dry',
                    'Use certified disease-free seed potatoes'
                ],
                'organic': 'Bacillus subtilis or copper-based fungicides applied preventatively'
            },
            'Tomato_healthy': {
                'treatment': 'Your plant is healthy! Continue good farming practices like proper watering and fertilization.',
                'amharic': 'የእርስዎ ተክል ጤናማ ነው! ትክክለኛ መጠጣት እና ማዳበሪያ አዝራሮችን ይቀጥሉ።',
                'prevention': [
                    'Continue regular monitoring',
                    'Maintain soil health with organic matter',
                    'Practice crop rotation',
                    'Watch for early signs of pests or diseases'
                ],
                'organic': 'Continue organic practices like composting and natural pest control'
            },
            'Potato___Late_blight': {
                'treatment': 'Apply fungicides containing metalaxyl or mancozeb. Destroy infected plants immediately.',
                'amharic': 'ሜታላክሲል ወይም ማንኮዜብ የያዙ ንጥረ ነገሮችን ይበጁ። የተበሳጩ ተክሎችን ወዲያውኑ ያጥፉ።',
                'prevention': [
                    'Use certified disease-free seed potatoes',
                    'Destroy volunteer potato plants',
                    'Avoid overhead irrigation',
                    'Harvest in dry weather'
                ],
                'organic': 'Copper-based fungicides and resistant varieties'
            }
        }
        
        # Default treatment for other diseases
        default = {
            'treatment': 'Consult local agricultural expert for specific treatment recommendations. Remove infected plant parts and improve growing conditions.',
            'amharic': 'ለተወሰኑ የሕክምና ምክሮች ከአካባቢዎ የሰብል ምሁር ይጠይቁ። የተበሳጩ የተክል ክፍሎችን ያስወግዱ እና የእድገት ሁኔታዎችን ያሻሽሉ።',
            'prevention': [
                'Practice crop rotation regularly',
                'Maintain soil health with organic matter',
                'Monitor plants regularly for early detection',
                'Use resistant varieties when available'
            ],
            'organic': 'Consult organic farming experts in your area for specific recommendations'
        }
        
        return treatment_db.get(disease_name, default)
    
    def test_prediction(self):
        """Test the predictor"""
        if self.model is None:
            print("❌ Model not loaded.")
            return
        
        print("✅ Real AI Disease Predictor is ready!")
        print(f"📊 Can identify: {len(self.class_names)} plant diseases")
        print(f"🎯 Training Accuracy: 96.34%")
        print("\n📝 Available diseases:")
        for i, disease in enumerate(self.class_names.keys(), 1):
            print(f"   {i:2d}. {disease}")

if __name__ == "__main__":
    predictor = RealDiseasePredictor()
    predictor.test_prediction()