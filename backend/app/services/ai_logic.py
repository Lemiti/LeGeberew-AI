import numpy as np
from PIL import Image
import io
import os

# Try to import tflite-runtime; fallback to a mock if not found for testing
try:
    import tflite_runtime.interpreter as tflite
    HAS_TFLITE = True
except ImportError:
    HAS_TFLITE = False

MODEL_PATH = "ml_models/plant_doctor.tflite"

# Mock Class Names - You will update these after training your model
CLASS_NAMES = ["Healthy Maize", "Maize Leaf Blight", "Potato Healthy", "Potato Early Blight", "Coffee Rust"]

def predict_disease(image_bytes: bytes):
    # 1. Check if model file exists
    if not os.path.exists(MODEL_PATH):
        return {
            "disease": "Demo Mode (Model File Missing)",
            "confidence": "100%",
            "note": f"Please place your trained model at {MODEL_PATH} later."
        }

    # 2. Preprocess the Image
    # Farmers take high-res photos; we must resize to 224x224 for MobileNetV2
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    
    # Convert image to a format the AI understands (Float32 and Normalized)
    input_data = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)

    # 3. Run Inference
    interpreter = tflite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    # 4. Get the Result
    output_data = interpreter.get_tensor(output_details[0]['index'])
    best_index = np.argmax(output_data[0])
    confidence = float(output_data[0][best_index])

    return {
        "disease": CLASS_NAMES[best_index],
        "confidence": f"{confidence:.2%}",
        "status": "Success"
    }