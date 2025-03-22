from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from treatment import analyzer

app = Flask(__name__)
# Enable CORS for the React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Constants from training
IMG_WIDTH = 224
IMG_HEIGHT = 224
CHANNELS = 3

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define class names
class_names = [
    'Pepper__Bacterial_spot',
    'Pepper__healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato_healthy'
]

# Load the model
try:
    model = tf.keras.models.load_model('Saved_Models/plant_disease_model.h5')
except Exception as e:
    model = None

def predict(img):
    """
    Process image and return prediction with treatment info
    """
    try:
        if model is None:
            raise RuntimeError("Model not loaded. Please ensure the model file exists and is valid.")
            
        if isinstance(img, Image.Image):
            img = img.resize((IMG_HEIGHT, IMG_WIDTH))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
        else:
            img_array = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])

        # Normalize and batch the image
        img_array = tf.expand_dims(img_array / 255.0, 0)
            
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Get the predicted class and confidence
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = float(100 * np.max(predictions[0]))

        # Get treatment info
        treatment_info = analyzer.get_treatment_info(predicted_class, confidence/100)
        
        return {
            "success": True,
            "prediction": predicted_class,
            "confidence": confidence,
            "treatment_info": treatment_info
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/predict', methods=['POST'])
def predict_api():
    try:
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file provided"
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": "Invalid file type. Allowed types: " + ', '.join(ALLOWED_EXTENSIONS)
            }), 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Load and process the image
            img = Image.open(filepath).convert('RGB')
            img = img.resize((IMG_WIDTH, IMG_HEIGHT))
            
            # Get prediction
            result = predict(img)
            
            return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)