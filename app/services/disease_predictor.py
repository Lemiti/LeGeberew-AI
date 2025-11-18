# ai/services/disease_predictor.py
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import os
from datetime import datetime

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.class_names = {}
        self.idx_to_class = {}
        self.load_model()
        
        # Treatment database
        self.treatment_db = self.load_treatment_database()
    
    def load_model(self):
        """Load trained model and class names"""
        try:
            self.model = tf.keras.models.load_model('ai/models/final_disease_model.h5')
            with open('ai/models/class_names.json', 'r') as f:
                self.class_names = json.load(f)
            self.idx_to_class = {v: k for k, v in self.class_names.items()}
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def load_treatment_database(self):
        """Load treatment recommendations database"""
        return {
            'Tomato_Early_blight': {
                'treatment': 'Apply copper-based fungicide every 7-10 days. Remove infected leaves.',
                'amharic': 'ከሚያስከትሉ ንጥረ ነገሮች ጋር የተለቀ ማር በየ 7-10 ቀናት ይበጁ። የተበሳጩ ቅጠሎችን ያስወግዱ።',
                'prevention': ['Rotate crops yearly', 'Ensure good air circulation', 'Water at base of plant'],
                'organic': 'Use neem oil or baking soda spray'
            },
            'Tomato_Late_blight': {
                'treatment': 'Apply fungicides containing chlorothalonil or mancozeb.',
                'amharic': 'ክሎሮታሎኒል ወይም ማንኮዜብ የያዙ ንጥረ ነገሮችን ይበጁ።',
                'prevention': ['Avoid overhead watering', 'Remove volunteer plants', 'Use resistant varieties'],
                'organic': 'Copper-based fungicides'
            },
            # Add more treatments for Ethiopian crops
            'Maize_Rust': {
                'treatment': 'Apply fungicide at first sign of disease. Use resistant varieties.',
                'amharic': 'የበሽታ ምልክት ሲታይ ንጥረ ነገር ይበጁ። የተቋቋሙ ዝርያዎችን ይጠቀሙ።',
                'prevention': ['Plant early', 'Ensure proper spacing', 'Remove crop debris'],
                'organic': 'Sulfur-based fungicides'
            }
        }
    
    def predict_disease(self, image_path):
        """Predict disease from image with enhanced results"""
        try:
            # Load and preprocess image
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0
            
            # Make prediction
            predictions = self.model.predict(img_array)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            predicted_class = self.idx_to_class[predicted_class_idx]
            
            # Get treatment information
            treatment_info = self.get_treatment_info(predicted_class)
            
            return {
                'disease': predicted_class,
                'confidence': float(confidence),
                'treatment_advice': treatment_info['treatment'],
                'amharic_advice': treatment_info['amharic'],
                'prevention_tips': treatment_info['prevention'],
                'organic_options': treatment_info['organic'],
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")
    
    def get_treatment_info(self, disease_name):
        """Get treatment information for detected disease"""
        default_treatment = {
            'treatment': 'Consult local agricultural expert for specific treatment recommendations.',
            'amharic': 'ለተወሰኑ የሕክምና ምክሮች ከአካባቢዎ የሰብል ምሁር ይጠይቁ።',
            'prevention': ['Practice crop rotation', 'Maintain soil health', 'Monitor plants regularly'],
            'organic': 'Consult organic farming experts'
        }
        
        return self.treatment_db.get(disease_name, default_treatment)