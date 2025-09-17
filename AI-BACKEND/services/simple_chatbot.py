"""
Simple Chatbot Service for JalBuddy
Handles greetings, basic conversations, and groundwater queries
"""

import re
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SimpleChatbot:
    """Simple rule-based chatbot for groundwater consultation"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        
        # Greeting patterns
        self.greeting_patterns = {
            'en': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening|namaste)\b',
                r'\b(how are you|what\'s up|how do you do)\b',
            ],
            'hi': [
                r'\b(नमस्ते|नमस्कार|हैलो|हाय|सलाम)\b',
                r'\b(कैसे हो|क्या हाल है|कैसे हैं)\b',
            ]
        }
        
        # Greeting responses
        self.greeting_responses = {
            'en': [
                "Hello! I'm JalBuddy, your groundwater assistant. How can I help you today?",
                "Hi there! I'm here to help with all your groundwater questions. What would you like to know?",
                "Namaste! I'm JalBuddy, ready to assist you with groundwater information. How may I help?",
                "Good to see you! I specialize in groundwater consultation. What's your query today?",
            ],
            'hi': [
                "नमस्ते! मैं जलबड्डी हूं, आपका भूजल सहायक। आज मैं आपकी कैसे मदद कर सकता हूं?",
                "नमस्कार! मैं भूजल संबंधी सभी प्रश्नों में आपकी सहायता के लिए हूं। आप क्या जानना चाहते हैं?",
                "हैलो! मैं जलबड्डी हूं, भूजल की जानकारी देने के लिए तैयार हूं। मैं आपकी कैसे मदद कर सकता हूं?",
                "आपसे मिलकर खुशी हुई! मैं भूजल परामर्श में विशेषज्ञ हूं। आज आपका क्या प्रश्न है?",
            ]
        }
        
        # Groundwater knowledge base
        self.knowledge_base = {
            'en': {
                'borewell': {
                    'patterns': [r'\b(borewell|bore well|drilling|dig well|tube well)\b'],
                    'responses': [
                        "For borewell construction, you need: 1) NOC from State Groundwater Authority, 2) Minimum 100m spacing from other wells, 3) Proper casing, 4) Don't exceed twice the static water level depth. Would you like specific guidelines for your area?",
                        "Borewell guidelines include getting permission, maintaining proper spacing, and following depth restrictions. The depth shouldn't exceed twice the static water level. Do you need information about permissions in your state?",
                    ]
                },
                'water_quality': {
                    'patterns': [r'\b(water quality|safe water|drinking water|TDS|fluoride|contamination)\b'],
                    'responses': [
                        "Water quality standards per IS 10500:2012: TDS <500mg/L (max 2000mg/L), Fluoride <1.0mg/L (max 1.5mg/L), pH 6.5-8.5. Regular testing is essential. Would you like to know about testing facilities in your area?",
                        "For safe drinking water, check TDS, fluoride, nitrate, and pH levels. TDS should be below 500mg/L for drinking. Do you have your water test results to discuss?",
                    ]
                },
                'gec_category': {
                    'patterns': [r'\b(GEC|category|classification|safe|critical|over.?exploited)\b'],
                    'responses': [
                        "GEC-2015 classifies groundwater into: Safe (<70% development), Semi-Critical (70-90%), Critical (90-100%), Over-Exploited (>100%). Which category information do you need?",
                        "Groundwater assessment follows GEC-2015 guidelines with four categories based on development stage and water level trends. What's your area's classification query?",
                    ]
                },
                'recharge': {
                    'patterns': [r'\b(recharge|rainwater harvest|check dam|percolation)\b'],
                    'responses': [
                        "Groundwater recharge methods: Check dams, percolation tanks, rooftop rainwater harvesting, recharge wells. Effectiveness varies: 15-25% in hard rock, 10-20% in alluvial areas. What recharge method interests you?",
                        "Rainwater harvesting and artificial recharge can boost groundwater. Methods include check dams, farm ponds, and rooftop collection. Would you like specific techniques for your geology?",
                    ]
                },
                'general': {
                    'patterns': [r'\b(groundwater|water level|monsoon|irrigation|farming)\b'],
                    'responses': [
                        "I can help with groundwater levels, quality testing, borewell guidelines, recharge methods, and GEC classifications. What specific aspect interests you?",
                        "Groundwater management involves monitoring levels, ensuring quality, following drilling norms, and implementing recharge. Which topic would you like to explore?",
                    ]
                }
            },
            'hi': {
                'borewell': {
                    'patterns': [r'\b(बोरवेल|बोर वेल|खुदाई|कुआं|ट्यूबवेल)\b'],
                    'responses': [
                        "बोरवेल निर्माण के लिए चाहिए: 1) राज्य भूजल प्राधिकरण से NOC, 2) अन्य कुओं से 100मी दूरी, 3) उचित केसिंग, 4) स्थिर जल स्तर से दोगुनी गहराई न करें। क्या आपको अपने क्षेत्र के लिए विशिष्ट दिशानिर्देश चाहिए?",
                        "बोरवेल दिशानिर्देशों में अनुमति लेना, उचित दूरी बनाए रखना, और गहराई की सीमा शामिल है। गहराई स्थिर जल स्तर से दोगुनी नहीं होनी चाहिए। क्या आपको अपने राज्य में अनुमति की जानकारी चाहिए?",
                    ]
                },
                'water_quality': {
                    'patterns': [r'\b(जल गुणवत्ता|सुरक्षित पानी|पीने का पानी|TDS|फ्लोराइड|प्रदूषण)\b'],
                    'responses': [
                        "जल गुणवत्ता मानक IS 10500:2012 के अनुसार: TDS <500mg/L (अधिकतम 2000mg/L), फ्लोराइड <1.0mg/L (अधिकतम 1.5mg/L), pH 6.5-8.5। नियमित जांच जरूरी है। क्या आपको अपने क्षेत्र की जांच सुविधाओं के बारे में जानना है?",
                        "सुरक्षित पीने के पानी के लिए TDS, फ्लोराइड, नाइट्रेट, और pH स्तर जांचें। पीने के लिए TDS 500mg/L से कम होना चाहिए। क्या आपके पास चर्चा के लिए पानी की जांच रिपोर्ट है?",
                    ]
                },
                'gec_category': {
                    'patterns': [r'\b(GEC|श्रेणी|वर्गीकरण|सुरक्षित|महत्वपूर्ण|अति.?दोहित)\b'],
                    'responses': [
                        "GEC-2015 भूजल को वर्गीकृत करता है: सुरक्षित (<70% विकास), अर्ध-महत्वपूर्ण (70-90%), महत्वपूर्ण (90-100%), अति-दोहित (>100%)। आपको कौन सी श्रेणी की जानकारी चाहिए?",
                        "भूजल मूल्यांकन GEC-2015 दिशानिर्देशों का पालन करता है जिसमें विकास चरण और जल स्तर प्रवृत्ति के आधार पर चार श्रेणियां हैं। आपके क्षेत्र का वर्गीकरण प्रश्न क्या है?",
                    ]
                },
                'recharge': {
                    'patterns': [r'\b(रिचार्ज|वर्षा जल संचयन|चेक डैम|पारगम्यता)\b'],
                    'responses': [
                        "भूजल रिचार्ज के तरीके: चेक डैम, पारगम्यता टैंक, छत वर्षा जल संचयन, रिचार्ज कुएं। प्रभावशीलता अलग होती है: हार्ड रॉक में 15-25%, जलोढ़ क्षेत्रों में 10-20%। कौन सा रिचार्ज तरीका आपकी दिलचस्पी का है?",
                        "वर्षा जल संचयन और कृत्रिम रिचार्ज से भूजल बढ़ाया जा सकता है। तरीकों में चेक डैम, फार्म तालाब, और छत संग्रह शामिल है। क्या आपको अपनी भूविज्ञान के लिए विशिष्ट तकनीकें चाहिए?",
                    ]
                },
                'general': {
                    'patterns': [r'\b(भूजल|जल स्तर|मानसून|सिंचाई|खेती)\b'],
                    'responses': [
                        "मैं भूजल स्तर, गुणवत्ता जांच, बोरवेल दिशानिर्देश, रिचार्ज तरीके, और GEC वर्गीकरण में मदद कर सकता हूं। कौन सा विशिष्ट पहलू आपकी रुचि का है?",
                        "भूजल प्रबंधन में स्तर निगरानी, गुणवत्ता सुनिश्चित करना, ड्रिलिंग नियम पालन, और रिचार्ज लागू करना शामिल है। आप कौन सा विषय अन्वेषण करना चाहते हैं?",
                    ]
                }
            }
        }
        
        # Fallback responses
        self.fallback_responses = {
            'en': [
                "I specialize in groundwater topics like borewell drilling, water quality, recharge methods, and GEC classifications. Could you ask about any of these areas?",
                "I'm here to help with groundwater questions. You can ask about water quality testing, borewell guidelines, or groundwater categories. What interests you?",
                "As a groundwater assistant, I can help with drilling permits, water testing, recharge techniques, and more. What specific information do you need?",
            ],
            'hi': [
                "मैं भूजल विषयों में विशेषज्ञ हूं जैसे बोरवेल खुदाई, जल गुणवत्ता, रिचार्ज तरीके, और GEC वर्गीकरण। क्या आप इन क्षेत्रों के बारे में पूछ सकते हैं?",
                "मैं भूजल प्रश्नों में मदद के लिए हूं। आप जल गुणवत्ता जांच, बोरवेल दिशानिर्देश, या भूजल श्रेणियों के बारे में पूछ सकते हैं। आपकी क्या रुचि है?",
                "भूजल सहायक के रूप में, मैं ड्रिलिंग अनुमति, पानी की जांच, रिचार्ज तकनीक, और अधिक में मदद कर सकता हूं। आपको क्या विशिष्ट जानकारी चाहिए?",
            ]
        }
        
    def detect_language(self, text: str) -> str:
        """Detect if text is in Hindi or English"""
        # Simple detection based on presence of Devanagari characters
        hindi_chars = re.search(r'[\u0900-\u097F]', text)
        return 'hi' if hindi_chars else 'en'
    
    def is_greeting(self, text: str, language: str) -> bool:
        """Check if the message is a greeting"""
        text_lower = text.lower()
        patterns = self.greeting_patterns.get(language, [])
        
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False
    
    def get_greeting_response(self, language: str) -> str:
        """Get a random greeting response"""
        responses = self.greeting_responses.get(language, self.greeting_responses['en'])
        return random.choice(responses)
    
    def find_best_response(self, text: str, language: str) -> Tuple[str, float]:
        """Find the best response for the given text"""
        text_lower = text.lower()
        best_response = ""
        best_confidence = 0.0
        
        # Check knowledge base for the language
        kb = self.knowledge_base.get(language, {})
        
        for topic, data in kb.items():
            patterns = data['patterns']
            responses = data['responses']
            
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    confidence = len(matches) * 0.3 + 0.7  # Base confidence + pattern matches
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_response = random.choice(responses)
        
        return best_response, best_confidence
    
    def get_fallback_response(self, language: str) -> str:
        """Get a fallback response when no pattern matches"""
        responses = self.fallback_responses.get(language, self.fallback_responses['en'])
        return random.choice(responses)
    
    def process_message(self, message: str, user_id: str = "default", context: Optional[Dict] = None) -> Dict:
        """Process a user message and return a response"""
        try:
            # Detect language
            language = self.detect_language(message)
            
            # Store context if provided
            if context:
                self.user_context[user_id] = context
            
            # Add to conversation history
            self.conversation_history.append({
                'user_id': user_id,
                'message': message,
                'language': language,
                'timestamp': datetime.now().isoformat()
            })
            
            # Check for greetings first
            if self.is_greeting(message, language):
                response = self.get_greeting_response(language)
                confidence = 0.95
                response_type = "greeting"
            else:
                # Find best response from knowledge base
                response, confidence = self.find_best_response(message, language)
                
                if confidence < 0.5:  # No good match found
                    response = self.get_fallback_response(language)
                    confidence = 0.5
                    response_type = "fallback"
                else:
                    response_type = "knowledge"
            
            # Personalize response if context available
            user_ctx = self.user_context.get(user_id, {})
            if user_ctx.get('location'):
                location = user_ctx['location']
                if language == 'hi':
                    response = response.replace("your area", f"{location} क्षेत्र")
                    response = response.replace("your state", f"{location} राज्य")
                else:
                    response = response.replace("your area", location)
                    response = response.replace("your state", f"{location} state")
            
            # Log the interaction
            logger.info(f"User ({language}): {message[:50]}...")
            logger.info(f"Bot response ({response_type}, {confidence:.2f}): {response[:50]}...")
            
            return {
                'response': response,
                'language': language,
                'confidence': confidence,
                'response_type': response_type,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            
            # Return error response
            error_msg = {
                'en': "I'm having trouble processing your message. Could you please try again?",
                'hi': "मुझे आपका संदेश प्रोसेस करने में समस्या हो रही है। कृपया फिर से कोशिश करें?"
            }
            
            lang = self.detect_language(message)
            return {
                'response': error_msg.get(lang, error_msg['en']),
                'language': lang,
                'confidence': 0.5,
                'response_type': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_conversation_history(self, user_id: str = "default", limit: int = 10) -> List[Dict]:
        """Get conversation history for a user"""
        user_history = [
            conv for conv in self.conversation_history 
            if conv['user_id'] == user_id
        ]
        return user_history[-limit:]
    
    def clear_history(self, user_id: str = "default"):
        """Clear conversation history for a user"""
        self.conversation_history = [
            conv for conv in self.conversation_history 
            if conv['user_id'] != user_id
        ]
        if user_id in self.user_context:
            del self.user_context[user_id]