# Plant Disease Detection 

A modern web application for detecting and analyzing plant diseases using deep learning and computer vision techniques.

## Features

- **Real-time Disease Detection**: Upload plant leaf images and get instant disease detection results
- **Symptom Analysis**: Advanced image processing to identify specific disease symptoms
- **Treatment Recommendations**: Get detailed treatment guides based on detected diseases
- **Multi-crop Support**: Supports multiple crops including:
  - Pepper (Bell Pepper)
  - Potato
  - Tomato

## Technology Stack

### Backend (Python)
- **Framework**: Flask
- **Deep Learning**: TensorFlow/Keras
- **Image Processing**: OpenCV, TensorFlow Image
- **Model**: Custom CNN trained on plant disease dataset
- **Features**: 
  - Color analysis (HSV color space)
  - Spot detection
  - Texture analysis
  - Symptom identification

### Frontend (React)
- **Framework**: React with TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: React Hooks
- **Features**:
  - Responsive design
  - Real-time feedback
  - Image preview
  - Treatment guide display

## Project Structure

```
.
├── app.py                 # Flask backend server
├── train.ipynb           # Model training notebook
├── Dataset/              # Training dataset
│   ├── Pepper/
│   ├── Potato/
│   └── Tomato/
├── Saved_Models/         # Trained model files
├── uploads/              # Temporary image upload directory
└── frontend/            # React frontend application
    ├── src/
    │   ├── components/  # React components
    │   └── utils/       # Utility functions
    └── public/          # Static files
```

## Installation

1. **Backend Setup**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd frontend
npm install
```

## Running the Application

1. **Start Backend Server**
```bash
python app.py
```
The server will start on http://localhost:5000

2. **Start Frontend Development Server**
```bash
cd frontend
npm start
```
The application will open in your browser at http://localhost:3000

## Model Architecture

The system uses a Convolutional Neural Network (CNN) trained on a large dataset of plant leaf images. The model architecture includes:
- Input layer (224x224x3)
- Multiple convolutional and pooling layers
- Dropout layers for regularization
- Dense layers with ReLU activation
- Softmax output layer for classification

## Image Analysis Pipeline

1. **Image Preprocessing**
   - Resize to 224x224
   - Normalize pixel values
   - Convert to appropriate color spaces

2. **Disease Detection**
   - Pass through trained CNN model
   - Get disease classification and confidence score

3. **Symptom Analysis**
   - Color analysis in HSV space
   - Spot detection using convolution
   - Texture analysis using variance

4. **Treatment Recommendation**
   - Match detected disease with treatment database
   - Provide customized recommendations based on symptoms

## Performance

- Model Accuracy: ~98% on test set
- Average Response Time: <2 seconds
- Supported Image Formats: JPEG, PNG
- Maximum Image Size: 5MB

## Future Improvements

1. **Model Enhancement**
   - Add support for more crop types
   - Improve accuracy for early-stage diseases
   - Implement disease severity estimation

2. **Feature Additions**
   - Mobile app development
   - Offline mode support
   - Multi-language support
   - Image enhancement tools

3. **System Optimization**
   - Model quantization for faster inference
   - Batch processing capability
   - Cloud deployment options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
