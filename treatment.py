from typing import Dict, List, Tuple
import json

class TreatmentAnalyzer:
    def __init__(self):
        # Dictionary containing disease information
        self.disease_info = {
            'Pepper__Bacterial_spot': {
                'symptoms': [
                    'Small, circular brown spots on leaves',
                    'Spots may have yellow halos',
                    'Lesions on fruits',
                    'Defoliation in severe cases'
                ],
                'treatment': [
                    'Remove infected plant debris',
                    'Use copper-based fungicides',
                    'Rotate crops with non-host plants',
                    'Avoid overhead irrigation'
                ],
                'severity_indicators': {
                    'mild': 'Few spots on some leaves',
                    'moderate': 'Multiple spots on many leaves',
                    'severe': 'Widespread infection and defoliation'
                }
            },
            'Pepper__healthy': {
                'symptoms': ['No visible symptoms', 'Normal leaf color', 'Healthy growth'],
                'treatment': ['Regular watering', 'Proper fertilization', 'Routine maintenance'],
                'severity_indicators': {'healthy': 'Plant showing normal growth patterns'}
            },
            'Potato___Early_blight': {
                'symptoms': [
                    'Dark brown spots with concentric rings',
                    'Yellow areas around spots',
                    'Lower leaves affected first',
                    'Leaf curling and death'
                ],
                'treatment': [
                    'Apply fungicides preventatively',
                    'Improve air circulation',
                    'Remove infected leaves',
                    'Maintain proper plant spacing'
                ],
                'severity_indicators': {
                    'mild': 'Few spots on lower leaves',
                    'moderate': 'Multiple spots on several leaves',
                    'severe': 'Widespread infection and leaf death'
                }
            },
            'Potato___Late_blight': {
                'symptoms': [
                    'Water-soaked spots on leaves',
                    'White fuzzy growth on undersides',
                    'Dark brown lesions on stems',
                    'Rapid plant collapse'
                ],
                'treatment': [
                    'Apply fungicides immediately',
                    'Remove infected plants',
                    'Increase plant spacing',
                    'Avoid overhead irrigation'
                ],
                'severity_indicators': {
                    'mild': 'Few water-soaked spots',
                    'moderate': 'Multiple spots with fuzzy growth',
                    'severe': 'Widespread infection and plant collapse'
                }
            },
            'Potato___healthy': {
                'symptoms': ['No visible symptoms', 'Normal leaf color', 'Healthy growth'],
                'treatment': ['Regular watering', 'Proper fertilization', 'Routine maintenance'],
                'severity_indicators': {'healthy': 'Plant showing normal growth patterns'}
            },
            'Tomato_Bacterial_spot': {
                'symptoms': [
                    'Small dark spots on leaves',
                    'Spots with yellow halos',
                    'Scabby lesions on fruits',
                    'Leaf yellowing and drop'
                ],
                'treatment': [
                    'Use copper-based sprays',
                    'Remove infected plants',
                    'Rotate crops',
                    'Avoid working with wet plants'
                ],
                'severity_indicators': {
                    'mild': 'Few spots on leaves',
                    'moderate': 'Multiple spots with fruit infection',
                    'severe': 'Widespread infection and defoliation'
                }
            },
            'Tomato_Early_blight': {
                'symptoms': [
                    'Dark brown spots with rings',
                    'Yellow tissue around spots',
                    'Lower leaf infection first',
                    'Stem lesions possible'
                ],
                'treatment': [
                    'Apply fungicides',
                    'Remove lower infected leaves',
                    'Improve air circulation',
                    'Mulch around plants'
                ],
                'severity_indicators': {
                    'mild': 'Few spots on lower leaves',
                    'moderate': 'Multiple spots on many leaves',
                    'severe': 'Widespread infection and defoliation'
                }
            },
            'Tomato_Late_blight': {
                'symptoms': [
                    'Large brown patches',
                    'White fuzzy growth',
                    'Rapid tissue death',
                    'Dark stem lesions'
                ],
                'treatment': [
                    'Apply protective fungicides',
                    'Remove infected plants',
                    'Improve drainage',
                    'Plant resistant varieties'
                ],
                'severity_indicators': {
                    'mild': 'Few patches on leaves',
                    'moderate': 'Multiple patches with fuzzy growth',
                    'severe': 'Widespread infection and plant death'
                }
            },
            'Tomato_Leaf_Mold': {
                'symptoms': [
                    'Yellow spots on upper leaf surface',
                    'Olive-green mold on undersides',
                    'Leaf curling and death',
                    'Higher humidity areas affected'
                ],
                'treatment': [
                    'Improve air circulation',
                    'Reduce humidity',
                    'Remove infected leaves',
                    'Apply fungicides if severe'
                ],
                'severity_indicators': {
                    'mild': 'Few yellow spots',
                    'moderate': 'Multiple spots with visible mold',
                    'severe': 'Widespread infection and leaf death'
                }
            },
            'Tomato_Septoria_leaf_spot': {
                'symptoms': [
                    'Small circular spots',
                    'Dark centers with light borders',
                    'Lower leaves first affected',
                    'Leaf yellowing and drop'
                ],
                'treatment': [
                    'Apply fungicides early',
                    'Remove infected leaves',
                    'Improve air circulation',
                    'Avoid overhead watering'
                ],
                'severity_indicators': {
                    'mild': 'Few spots on lower leaves',
                    'moderate': 'Multiple spots on several leaves',
                    'severe': 'Widespread infection and defoliation'
                }
            },
            'Tomato_Spider_mites_Two_spotted_spider_mite': {
                'symptoms': [
                    'Tiny yellow spots on leaves',
                    'Webbing on leaves',
                    'Leaf bronzing',
                    'Plant stunting'
                ],
                'treatment': [
                    'Apply miticides',
                    'Increase humidity',
                    'Remove heavily infested leaves',
                    'Use natural predators'
                ],
                'severity_indicators': {
                    'mild': 'Few spots, minimal webbing',
                    'moderate': 'Multiple spots with visible webbing',
                    'severe': 'Extensive damage and heavy webbing'
                }
            },
            'Tomato__Target_Spot': {
                'symptoms': [
                    'Circular brown spots',
                    'Concentric rings in spots',
                    'Leaf yellowing',
                    'Fruit spots possible'
                ],
                'treatment': [
                    'Apply fungicides',
                    'Improve air circulation',
                    'Remove infected tissue',
                    'Maintain proper spacing'
                ],
                'severity_indicators': {
                    'mild': 'Few target-like spots',
                    'moderate': 'Multiple spots on leaves and fruit',
                    'severe': 'Widespread infection on plant'
                }
            },
            'Tomato__Tomato_YellowLeaf__Curl_Virus': {
                'symptoms': [
                    'Leaf curling and yellowing',
                    'Stunted growth',
                    'Flower drop',
                    'Reduced fruit production'
                ],
                'treatment': [
                    'Remove infected plants',
                    'Control whiteflies',
                    'Use resistant varieties',
                    'Install physical barriers'
                ],
                'severity_indicators': {
                    'mild': 'Slight leaf curling',
                    'moderate': 'Noticeable curling and yellowing',
                    'severe': 'Severe curling and stunting'
                }
            },
            'Tomato_healthy': {
                'symptoms': ['No visible symptoms', 'Normal leaf color', 'Healthy growth'],
                'treatment': ['Regular watering', 'Proper fertilization', 'Routine maintenance'],
                'severity_indicators': {'healthy': 'Plant showing normal growth patterns'}
            }
        }

    def get_treatment_info(self, disease_class: str, confidence: float) -> Dict:
        """
        Get treatment information based on disease class and confidence score
        """
        if disease_class not in self.disease_info:
            return {
                'error': 'Disease class not found',
                'status': 'unknown'
            }

        info = self.disease_info[disease_class]
        
        # Determine severity based on confidence score
        severity = self._determine_severity(confidence)
        
        return {
            'disease': disease_class,
            'confidence': confidence,
            'severity': severity,
            'symptoms': info['symptoms'],
            'treatment': info['treatment'],
            'severity_description': info['severity_indicators'].get(severity, 'Unknown severity')
        }

    def _determine_severity(self, confidence: float) -> str:
        """
        Determine severity based on confidence score
        """
        if confidence < 0.5:
            return 'mild'
        elif confidence < 0.8:
            return 'moderate'
        else:
            return 'severe'

    def get_all_diseases(self) -> List[str]:
        """
        Get list of all diseases
        """
        return list(self.disease_info.keys())

# Create an instance of the analyzer
analyzer = TreatmentAnalyzer()
