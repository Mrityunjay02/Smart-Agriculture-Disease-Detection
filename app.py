from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from treatment import analyzer
import requests
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
# Enable CORS for the React frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Constants from training
IMG_WIDTH = 224
IMG_HEIGHT = 224
CHANNELS = 3
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Model configuration
MODEL_PATH = os.path.join('Saved_Models', 'plant_disease_model.h5')

# Load the model at startup
def load_model_safe():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"Successfully loaded model from {MODEL_PATH}")
            return True
        else:
            print(f"Error: Model file not found at {MODEL_PATH}")
            print("Please ensure you have:")
            print("1. Trained the model and saved it as 'plant_disease_model.h5'")
            print("2. Placed the model file in the 'Saved_Models' directory")
            print("3. The model file has the correct permissions")
            model = None
            return False
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        model = None
        return False

# Initialize model
model = None
model_loaded = load_model_safe()

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

# Weather API key (replace with your OpenWeatherMap API key)
WEATHER_API_KEY = 'your_openweather_api_key'

# Soil quality thresholds
SOIL_PH_RANGES = {
    'poor': (0, 4.5),
    'moderate': (4.5, 6.5),
    'good': (6.5, 7.5)
}

SOIL_MOISTURE_RANGES = {
    'poor': (0, 30),
    'moderate': (30, 60),
    'good': (60, 100)
}

# Crop rotation database
CROP_ROTATION_DB = {
    'tomato': {
        'next_crops': ['beans', 'peas', 'corn', 'cabbage'],
        'rotation_period': '3-4 months',
        'soil_ph': (6.0, 6.8),
        'soil_moisture': (50, 80)
    },
    'potato': {
        'next_crops': ['beans', 'corn', 'peas'],
        'rotation_period': '2-3 months',
        'soil_ph': (5.0, 6.5),
        'soil_moisture': (60, 85)
    }
}

# Mock database (replace with real database in production)
posts_db = []
experts_db = []
consultations_db = []

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

        # Extract plant name from prediction
        plant_name = predicted_class.split('_')[0]  # e.g., "Tomato" from "Tomato_healthy"
        disease_name = '_'.join(predicted_class.split('_')[1:])  # e.g., "healthy" or "Bacterial_spot"

        # Get treatment info
        treatment_info = analyzer.get_treatment_info(predicted_class)
        
        return {
            "success": True,
            "plant": plant_name,
            "disease": disease_name if disease_name else "healthy",
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
    # Check if model is loaded
    if model is None:
        return jsonify({
            "success": False,
            "error": "Model not loaded. Please check server logs."
        }), 500

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "error": "No file part in the request"
        }), 400
    
    file = request.files['file']
    
    # If user does not select file
    if file.filename == '':
        return jsonify({
            "success": False,
            "error": "No file selected"
        }), 400
        
    # Check file size
    if request.content_length > MAX_CONTENT_LENGTH:
        return jsonify({
            "success": False,
            "error": f"File too large. Maximum size is {MAX_CONTENT_LENGTH/(1024*1024)}MB"
        }), 413
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Open and process the image
            with Image.open(filepath) as img:
                result = predict(img)
                
            # Clean up the uploaded file
            os.remove(filepath)
            return jsonify(result)
            
        except Exception as e:
            # Clean up file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                "success": False,
                "error": f"Error processing image: {str(e)}"
            }), 500
    
    return jsonify({
        "success": False,
        "error": "Invalid file type. Allowed types are: " + ", ".join(ALLOWED_EXTENSIONS)
    }), 400

@app.route('/api/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    try:
        # Get coordinates from location name
        geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={WEATHER_API_KEY}'
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data:
            return jsonify({'error': 'Location not found'}), 404

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Get weather data
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        rainfall = weather_data.get('rain', {}).get('1h', 0)

        # Calculate disease risk based on weather conditions
        disease_risk = calculate_disease_risk(temperature, humidity, rainfall)

        return jsonify({
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'forecast': weather_data['weather'][0]['description'],
            'diseaseRisk': disease_risk
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/soil-analysis', methods=['POST'])
def analyze_soil():
    data = request.get_json()
    ph = data.get('ph')
    moisture = data.get('moisture')

    if ph is None or moisture is None:
        return jsonify({'error': 'Both pH and moisture are required'}), 400

    try:
        # Determine soil quality
        quality = determine_soil_quality(ph, moisture)
        
        # Generate recommendations
        recommendations = generate_soil_recommendations(ph, moisture, quality)

        return jsonify({
            'ph': ph,
            'moisture': moisture,
            'quality': quality,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crop-rotation', methods=['POST'])
def get_crop_rotation():
    data = request.get_json()
    current_crop = data.get('currentCrop')
    soil_ph = data.get('soilPH')
    soil_moisture = data.get('soilMoisture')
    weather = data.get('weather')

    if not all([current_crop, soil_ph, soil_moisture, weather]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        rotation_data = CROP_ROTATION_DB.get(current_crop.lower())
        if not rotation_data:
            return jsonify({'error': 'Crop not found in database'}), 404

        # Filter suitable crops based on conditions
        suitable_crops = filter_suitable_crops(
            rotation_data['next_crops'],
            soil_ph,
            soil_moisture,
            weather
        )

        return jsonify({
            'currentCrop': current_crop,
            'nextRecommendedCrops': suitable_crops,
            'rotationPeriod': rotation_data['rotation_period'],
            'reasoning': generate_rotation_reasoning(suitable_crops, soil_ph, soil_moisture, weather)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts_db)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'content': data['content'],
        'tags': data['tags'],
        'author': {
            'name': 'Current User',  # Replace with actual user data
            'avatar': 'https://example.com/avatar.jpg'
        },
        'likes': 0,
        'comments': [],
        'createdAt': datetime.now().isoformat()
    }
    posts_db.insert(0, post)
    return jsonify(post)

@app.route('/api/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if post:
        post['likes'] += 1
        return jsonify({'success': True})
    return jsonify({'error': 'Post not found'}), 404

@app.route('/api/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    comment = {
        'id': str(uuid.uuid4()),
        'content': data['content'],
        'author': {
            'name': 'Current User',  # Replace with actual user data
            'avatar': 'https://example.com/avatar.jpg'
        },
        'createdAt': datetime.now().isoformat()
    }
    post['comments'].append(comment)
    return jsonify(comment)

@app.route('/api/experts', methods=['GET'])
def get_experts():
    return jsonify(experts_db)

@app.route('/api/consultations', methods=['POST'])
def book_consultation():
    data = request.get_json()
    expert = next((e for e in experts_db if e['id'] == data['expertId']), None)
    if not expert:
        return jsonify({'error': 'Expert not found'}), 404

    consultation = {
        'id': str(uuid.uuid4()),
        'expertId': data['expertId'],
        'userId': 'current_user_id',  # Replace with actual user ID
        'date': data['date'],
        'topic': data['topic'],
        'description': data['description'],
        'preferredLanguage': data['preferredLanguage'],
        'status': 'scheduled',
        'createdAt': datetime.now().isoformat()
    }
    consultations_db.append(consultation)
    return jsonify(consultation)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # Basic response for disease-related queries
    if 'disease' in message or 'symptoms' in message:
        response = "I can help identify plant diseases through image analysis. Would you like to upload a photo of your plant?"
    else:
        response = "I'm here to help with plant disease detection. Would you like to upload an image for analysis?"

    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

def calculate_disease_risk(temperature, humidity, rainfall):
    # High risk conditions:
    # - High humidity (>80%) and moderate temperature (20-30°C)
    # - Recent rainfall and high humidity
    risk_score = 0
    
    if 20 <= temperature <= 30:
        risk_score += 1
    if humidity > 80:
        risk_score += 2
    if rainfall > 0:
        risk_score += 1

    if risk_score >= 3:
        return 'high'
    elif risk_score == 2:
        return 'medium'
    return 'low'

def determine_soil_quality(ph, moisture):
    ph_quality = 'poor'
    moisture_quality = 'poor'

    for quality, (min_val, max_val) in SOIL_PH_RANGES.items():
        if min_val <= ph <= max_val:
            ph_quality = quality
            break

    for quality, (min_val, max_val) in SOIL_MOISTURE_RANGES.items():
        if min_val <= moisture <= max_val:
            moisture_quality = quality
            break

    # Overall quality is the lower of the two
    quality_ranks = ['poor', 'moderate', 'good']
    return min(ph_quality, moisture_quality, key=lambda x: quality_ranks.index(x))

def generate_soil_recommendations(ph, moisture, quality):
    recommendations = []

    if quality == 'poor':
        if ph < 6.0:
            recommendations.append('Add agricultural lime to increase soil pH')
        elif ph > 7.5:
            recommendations.append('Add sulfur to decrease soil pH')

        if moisture < 30:
            recommendations.append('Improve irrigation and add organic matter to increase water retention')
        elif moisture > 80:
            recommendations.append('Improve drainage and reduce watering frequency')

    elif quality == 'moderate':
        recommendations.append('Add organic matter to improve soil structure')
        if ph < 6.5:
            recommendations.append('Gradually increase pH with small amounts of lime')
        if moisture < 60:
            recommendations.append('Consider mulching to retain moisture')

    else:  # good
        recommendations.append('Maintain current soil conditions')
        recommendations.append('Regular monitoring of pH and moisture levels')

    return recommendations

def filter_suitable_crops(crops, soil_ph, soil_moisture, weather):
    suitable_crops = []
    
    for crop in crops:
        crop_data = CROP_ROTATION_DB.get(crop)
        if not crop_data:
            continue

        # Check if conditions match crop requirements
        ph_range = crop_data['soil_ph']
        moisture_range = crop_data['soil_moisture']

        if (ph_range[0] <= soil_ph <= ph_range[1] and
            moisture_range[0] <= soil_moisture <= moisture_range[1]):
            suitable_crops.append(crop)

    return suitable_crops

def generate_rotation_reasoning(crops, soil_ph, soil_moisture, weather):
    reasons = []
    
    if not crops:
        reasons.append('Current conditions are not optimal for most crops')
    else:
        reasons.append(f'Selected crops are suitable for soil pH {soil_ph} and moisture {soil_moisture}%')
        
    if weather['diseaseRisk'] == 'high':
        reasons.append('Consider disease-resistant varieties due to high risk conditions')
    
    return ' '.join(reasons)

if __name__ == '__main__':
    app.run(debug=True, port=5000)