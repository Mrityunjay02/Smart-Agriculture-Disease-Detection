# Smart Agriculture - Plant Disease Detection 

An AI-powered agricultural assistant that helps farmers detect and manage plant diseases through image analysis and intelligent recommendations.

## Features

### 1. Plant Disease Detection
- Upload leaf images for instant disease analysis
- Advanced AI-powered disease recognition
- Confidence score for disease detection
- Severity level assessment (Low/Medium/High)

### 2. Smart Analysis
- Detailed symptom identification
- Customized treatment recommendations
- Prevention measures and best practices
- Historical analysis tracking

### 3. User-Friendly Interface
- Interactive chat interface with Farmer AI
- Voice input support for queries
- Image gallery for tracking plant health
- Easy-to-read analysis reports

### 4. Analysis History
- Save and track all plant analyses
- Monitor disease progression
- View historical data through chips
- Track treatment effectiveness

## Technical Stack

### Frontend
- React.js with TypeScript
- Web Speech API for voice recognition
- Local Storage for analysis history
- Responsive design for all devices

### AI/ML
- Google Gemini API for image analysis
- Advanced prompt engineering
- Multi-language support
- Real-time processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mrityunjay02/Smart-Agriculture-Disease-Detection.git
```

2. Install dependencies:
```bash
cd frontend
npm install
```

3. Set up environment variables:
Create a `.env` file in the frontend directory:
```
REACT_APP_GEMINI_API_KEY=your_api_key_here
```

4. Start the development server:
```bash
npm start
```

## Environment Variables

- `REACT_APP_GEMINI_API_KEY`: Google Gemini API key for image analysis

## Usage

1. **Upload Image**:
   - Click the upload button or drag & drop a leaf image
   - The AI will automatically analyze the image

2. **View Analysis**:
   - Get instant disease detection results
   - View detailed symptoms and treatment plan
   - Check severity level and recommendations

3. **Track History**:
   - Click on history chips to view past analyses
   - Monitor plant health over time
   - Track treatment progress

4. **Voice Interaction**:
   - Click the microphone button
   - Ask questions about plant health
   - Get voice responses

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini API for powerful image analysis
- React.js community for excellent tools and libraries
- Contributors and testers who helped improve the system
