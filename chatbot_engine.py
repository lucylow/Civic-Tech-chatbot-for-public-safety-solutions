import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class ChatbotEngine:
    """
    Core chatbot engine for SafeIndy AI public safety chatbot.
    Handles intent recognition, entity extraction, and response generation.
    """
    
    def __init__(self):
        self.intents = self._load_intents()
        self.responses = self._load_responses()
        self.emergency_keywords = [
            'emergency', 'urgent', 'help', 'danger', 'fire', 'accident', 
            'injured', 'hurt', 'bleeding', 'unconscious', 'robbery', 
            'assault', 'shooting', 'stabbing', 'overdose', 'heart attack',
            'stroke', 'choking', 'drowning', 'trapped', 'explosion'
        ]
        
    def _load_intents(self) -> Dict:
        """Load intent patterns and classifications"""
        return {
            'emergency': {
                'patterns': [
                    r'\b(emergency|urgent|help|danger|911)\b',
                    r'\b(fire|accident|injured|hurt|bleeding)\b',
                    r'\b(robbery|assault|shooting|stabbing)\b',
                    r'\b(heart attack|stroke|choking|overdose)\b'
                ],
                'confidence_threshold': 0.8
            },
            'hazard_report': {
                'patterns': [
                    r'\b(report|hazard|problem|issue|pothole)\b',
                    r'\b(broken|damaged|dangerous|unsafe)\b',
                    r'\b(road|street|sidewalk|bridge|traffic)\b',
                    r'\b(flooding|debris|obstruction)\b'
                ],
                'confidence_threshold': 0.6
            },
            'information': {
                'patterns': [
                    r'\b(what|how|where|when|why)\b',
                    r'\b(information|help|guide|tips)\b',
                    r'\b(safety|prepare|prevention)\b',
                    r'\b(contact|phone|number|address)\b'
                ],
                'confidence_threshold': 0.5
            },
            'alerts': {
                'patterns': [
                    r'\b(alert|notification|warning|update)\b',
                    r'\b(weather|traffic|emergency|news)\b',
                    r'\b(current|active|recent)\b'
                ],
                'confidence_threshold': 0.6
            },
            'greeting': {
                'patterns': [
                    r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
                    r'\b(start|begin|help me)\b'
                ],
                'confidence_threshold': 0.7
            }
        }
    
    def _load_responses(self) -> Dict:
        """Load response templates for different intents"""
        return {
            'emergency': {
                'high_priority': {
                    'message': "🚨 **EMERGENCY DETECTED** 🚨\n\nIf this is a life-threatening emergency, **CALL 911 IMMEDIATELY**.\n\nI can provide guidance while you wait for help. What's the nature of the emergency?",
                    'quick_actions': [
                        {'text': '🚑 Call 911 Now', 'action': 'call_911'},
                        {'text': '🩹 First Aid Guide', 'action': 'first_aid'},
                        {'text': '📍 Share Location', 'action': 'share_location'}
                    ]
                },
                'medium_priority': {
                    'message': "I understand you need help. If this is a life-threatening emergency, please call 911 immediately.\n\nFor non-emergency assistance, I can help you:\n• Report safety concerns\n• Find emergency services\n• Get safety information\n\nWhat type of help do you need?",
                    'quick_actions': [
                        {'text': '📋 Report Issue', 'action': 'report_hazard'},
                        {'text': '📞 Emergency Contacts', 'action': 'emergency_contacts'},
                        {'text': '🏥 Find Services', 'action': 'find_services'}
                    ]
                }
            },
            'hazard_report': {
                'message': "I'll help you report a safety hazard. Please provide the following information:\n\n📍 **Location**: Where is the hazard?\n📝 **Description**: What type of hazard is it?\n📷 **Photo**: Can you take a picture? (optional)\n\nWhat type of hazard would you like to report?",
                'quick_actions': [
                    {'text': '🚧 Road/Traffic Hazard', 'action': 'report_road'},
                    {'text': '🏗️ Infrastructure Issue', 'action': 'report_infrastructure'},
                    {'text': '🌳 Environmental Concern', 'action': 'report_environmental'},
                    {'text': '👥 Public Safety Issue', 'action': 'report_safety'}
                ]
            },
            'information': {
                'message': "I can provide information about:\n\n🛡️ **Safety Tips & Guidelines**\n📞 **Emergency Contacts & Services**\n🏢 **City Services & Resources**\n🌦️ **Weather & Traffic Updates**\n📋 **How to Report Issues**\n\nWhat information are you looking for?",
                'quick_actions': [
                    {'text': '🛡️ Safety Tips', 'action': 'safety_tips'},
                    {'text': '📞 Emergency Contacts', 'action': 'emergency_contacts'},
                    {'text': '🏢 City Services', 'action': 'city_services'},
                    {'text': '🌦️ Current Alerts', 'action': 'current_alerts'}
                ]
            },
            'alerts': {
                'message': "Here are the current alerts and notifications for Indianapolis:\n\nI can show you:\n• Active emergency alerts\n• Weather warnings\n• Traffic updates\n• Community notifications\n\nWhat type of alerts would you like to see?",
                'quick_actions': [
                    {'text': '🚨 Emergency Alerts', 'action': 'emergency_alerts'},
                    {'text': '🌦️ Weather Alerts', 'action': 'weather_alerts'},
                    {'text': '🚗 Traffic Updates', 'action': 'traffic_alerts'},
                    {'text': '📢 Community News', 'action': 'community_alerts'}
                ]
            },
            'greeting': {
                'message': "Hello! I'm **SafeIndy AI**, your 24/7 public safety assistant for Indianapolis. I'm here to help with:\n\n🚨 **Emergency Assistance**\n📋 **Hazard Reporting**\n📢 **Safety Alerts & Information**\n📞 **Emergency Contacts & Services**\n\nHow can I help keep you safe today?",
                'quick_actions': [
                    {'text': '🚨 Emergency Help', 'action': 'emergency'},
                    {'text': '📋 Report Hazard', 'action': 'report_hazard'},
                    {'text': '📢 View Alerts', 'action': 'view_alerts'},
                    {'text': '❓ Safety Info', 'action': 'safety_info'}
                ]
            },
            'fallback': {
                'message': "I'm not sure I understand. I'm SafeIndy AI, and I can help you with:\n\n• Emergency assistance and 911 guidance\n• Reporting safety hazards and issues\n• Current alerts and notifications\n• Safety information and resources\n\nCould you please rephrase your request or choose one of the options below?",
                'quick_actions': [
                    {'text': '🚨 Emergency', 'action': 'emergency'},
                    {'text': '📋 Report Issue', 'action': 'report_hazard'},
                    {'text': '📢 Alerts', 'action': 'view_alerts'},
                    {'text': '❓ Information', 'action': 'safety_info'}
                ]
            }
        }
    
    def classify_intent(self, message: str) -> Tuple[str, float]:
        """
        Classify the intent of a user message.
        Returns (intent, confidence_score)
        """
        message_lower = message.lower()
        
        # Check for emergency keywords first (highest priority)
        emergency_score = self._calculate_pattern_score(message_lower, self.intents['emergency']['patterns'])
        if emergency_score >= self.intents['emergency']['confidence_threshold']:
            return 'emergency', emergency_score
        
        # Check other intents
        best_intent = 'fallback'
        best_score = 0.0
        
        for intent, config in self.intents.items():
            if intent == 'emergency':  # Already checked
                continue
                
            score = self._calculate_pattern_score(message_lower, config['patterns'])
            if score >= config['confidence_threshold'] and score > best_score:
                best_intent = intent
                best_score = score
        
        return best_intent, best_score
    
    def _calculate_pattern_score(self, message: str, patterns: List[str]) -> float:
        """Calculate confidence score based on pattern matching"""
        total_matches = 0
        total_patterns = len(patterns)
        
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                total_matches += 1
        
        return total_matches / total_patterns if total_patterns > 0 else 0.0
    
    def extract_entities(self, message: str, intent: str) -> Dict:
        """Extract relevant entities from the message based on intent"""
        entities = {}
        message_lower = message.lower()
        
        if intent == 'emergency':
            # Extract emergency type
            emergency_types = {
                'medical': r'\b(heart attack|stroke|choking|overdose|injured|hurt|bleeding|unconscious)\b',
                'fire': r'\b(fire|smoke|burning|explosion)\b',
                'crime': r'\b(robbery|assault|shooting|stabbing|theft|break.?in)\b',
                'accident': r'\b(accident|crash|collision|vehicle)\b'
            }
            
            for etype, pattern in emergency_types.items():
                if re.search(pattern, message_lower):
                    entities['emergency_type'] = etype
                    break
        
        elif intent == 'hazard_report':
            # Extract hazard category
            hazard_types = {
                'road_traffic': r'\b(pothole|road|street|traffic|sign|light|intersection)\b',
                'infrastructure': r'\b(bridge|sidewalk|building|structure|utility|pipe|wire)\b',
                'environmental': r'\b(flooding|debris|tree|pollution|spill|waste)\b',
                'public_safety': r'\b(lighting|security|vandalism|graffiti|suspicious)\b'
            }
            
            for htype, pattern in hazard_types.items():
                if re.search(pattern, message_lower):
                    entities['hazard_category'] = htype
                    break
        
        # Extract location information
        location_patterns = [
            r'\b(\d+)\s+([A-Za-z\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln|way|circle|cir|court|ct))\b',
            r'\bnear\s+([A-Za-z\s]+)\b',
            r'\bat\s+([A-Za-z\s]+)\b',
            r'\bon\s+([A-Za-z\s]+(?:street|st|avenue|ave|road|rd))\b'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                entities['location'] = match.group(0)
                break
        
        return entities
    
    def generate_response(self, intent: str, entities: Dict, context: Dict = None) -> Dict:
        """Generate appropriate response based on intent and entities"""
        
        if intent == 'emergency':
            # Determine emergency priority
            emergency_type = entities.get('emergency_type')
            if emergency_type in ['medical', 'fire', 'crime']:
                response_data = self.responses['emergency']['high_priority']
            else:
                response_data = self.responses['emergency']['medium_priority']
        else:
            response_data = self.responses.get(intent, self.responses['fallback'])
        
        # Customize response based on entities
        message = response_data['message']
        quick_actions = response_data.get('quick_actions', [])
        
        # Add context-specific information
        if entities.get('location'):
            message += f"\n\n📍 **Location detected**: {entities['location']}"
        
        if entities.get('hazard_category'):
            category_names = {
                'road_traffic': 'Road/Traffic Hazard',
                'infrastructure': 'Infrastructure Issue',
                'environmental': 'Environmental Concern',
                'public_safety': 'Public Safety Issue'
            }
            category_name = category_names.get(entities['hazard_category'], 'General Hazard')
            message += f"\n\n📋 **Category**: {category_name}"
        
        return {
            'message': message,
            'quick_actions': quick_actions,
            'intent': intent,
            'entities': entities,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def process_message(self, message: str, context: Dict = None) -> Dict:
        """
        Main method to process a user message and generate response.
        Returns complete response with intent, entities, and generated message.
        """
        # Classify intent
        intent, confidence = self.classify_intent(message)
        
        # Extract entities
        entities = self.extract_entities(message, intent)
        
        # Generate response
        response = self.generate_response(intent, entities, context)
        
        # Add metadata
        response.update({
            'confidence': confidence,
            'original_message': message
        })
        
        return response
    
    def get_safety_tips(self, category: str = 'general') -> Dict:
        """Get safety tips for specific categories"""
        tips = {
            'general': [
                "Always be aware of your surroundings",
                "Keep emergency contacts readily available",
                "Trust your instincts - if something feels wrong, seek help",
                "Stay informed about local alerts and warnings"
            ],
            'weather': [
                "Monitor weather alerts and warnings",
                "Have an emergency kit ready",
                "Know your evacuation routes",
                "Stay indoors during severe weather"
            ],
            'traffic': [
                "Always wear your seatbelt",
                "Don't text and drive",
                "Maintain safe following distance",
                "Report dangerous road conditions"
            ],
            'home': [
                "Install smoke and carbon monoxide detectors",
                "Keep doors and windows locked",
                "Have a family emergency plan",
                "Know your neighbors"
            ]
        }
        
        return {
            'category': category,
            'tips': tips.get(category, tips['general']),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_emergency_contacts(self) -> Dict:
        """Get emergency contact information for Indianapolis"""
        return {
            'emergency': {
                'name': 'Emergency Services (Police, Fire, EMS)',
                'number': '911',
                'description': 'Life-threatening emergencies only'
            },
            'non_emergency': {
                'police': {
                    'name': 'IMPD Non-Emergency',
                    'number': '(317) 327-3811',
                    'description': 'Non-emergency police matters'
                },
                'fire': {
                    'name': 'IFD Non-Emergency',
                    'number': '(317) 327-3811',
                    'description': 'Non-emergency fire department'
                }
            },
            'city_services': {
                'mayor_hotline': {
                    'name': "Mayor's Action Center",
                    'number': '(317) 327-4622',
                    'description': 'City services and complaints'
                },
                'public_works': {
                    'name': 'Public Works',
                    'number': '(317) 327-4622',
                    'description': 'Road issues, potholes, infrastructure'
                }
            },
            'crisis_support': {
                'mental_health': {
                    'name': 'Crisis & Suicide Lifeline',
                    'number': '988',
                    'description': '24/7 mental health crisis support'
                },
                'domestic_violence': {
                    'name': 'Domestic Violence Hotline',
                    'number': '1-800-799-7233',
                    'description': '24/7 domestic violence support'
                }
            }
        }

