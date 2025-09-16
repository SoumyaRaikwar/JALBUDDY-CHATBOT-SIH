import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  en: {
    translation: {
      "welcome_message": "Hello! I'm JalBuddy, your AI assistant for groundwater information. How can I help you today?",
      "input_placeholder": "Type your groundwater query here...",
      "voice_input_start": "Start voice input",
      "voice_input_stop": "Stop recording",
      "send_message": "Send message",
      "enable_voice": "Enable voice output",
      "disable_voice": "Disable voice output",
      "switch_to_hindi": "Switch to Hindi",
      "switch_to_english": "Switch to English",
      "groundwater_assistant": "Groundwater Information Assistant",
      "responses": {
        "groundwater_info": "I can help you with groundwater information! Are you looking for data about water levels, quality, or availability in a specific area? Please specify your location or district.",
        "rainfall_info": "Rainfall data is crucial for groundwater recharge. I can provide information about seasonal patterns and their impact on groundwater levels. Which region are you interested in?",
        "boring_info": "For boring/drilling information, I can guide you on optimal locations based on groundwater data, geological surveys, and success rates in your area. What's your location?",
        "quality_info": "Water quality is essential for safe consumption. I can provide information about groundwater quality parameters, contamination levels, and treatment recommendations for your area.",
        "default": "I understand you're looking for groundwater-related information. You can ask me about water levels, quality, rainfall impact, boring locations, or any other groundwater queries. How specifically can I assist you?"
      }
    }
  },
  hi: {
    translation: {
      "welcome_message": "नमस्ते! मैं जलबडी हूं, भूजल जानकारी के लिए आपका AI सहायक। आज मैं आपकी कैसे मदद कर सकता हूं?",
      "input_placeholder": "यहाँ अपना भूजल प्रश्न लिखें...",
      "voice_input_start": "वॉयस इनपुट शुरू करें",
      "voice_input_stop": "रिकॉर्डिंग बंद करें",
      "send_message": "संदेश भेजें",
      "enable_voice": "आवाज आउटपुट सक्षम करें",
      "disable_voice": "आवाज आउटपुट अक्षम करें",
      "switch_to_hindi": "हिंदी में स्विच करें",
      "switch_to_english": "अंग्रेजी में स्विच करें",
      "groundwater_assistant": "भूजल सूचना सहायक",
      "responses": {
        "groundwater_info": "मैं आपको भूजल की जानकारी में मदद कर सकता हूं! क्या आप किसी विशिष्ट क्षेत्र में जल स्तर, गुणवत्ता या उपलब्धता के बारे में डेटा चाहते हैं? कृपया अपना स्थान या जिला बताएं।",
        "rainfall_info": "वर्षा डेटा भूजल रिचार्ज के लिए महत्वपूर्ण है। मैं मौसमी पैटर्न और भूजल स्तर पर उनके प्रभाव के बारे में जानकारी प्रदान कर सकता हूं। आप किस क्षेत्र में रुचि रखते हैं?",
        "boring_info": "बोरिंग/ड्रिलिंग जानकारी के लिए, मैं भूजल डेटा, भूवैज्ञानिक सर्वेक्षण और आपके क्षेत्र में सफलता दर के आधार पर इष्टतम स्थानों पर मार्गदर्शन कर सकता हूं। आपका स्थान क्या है?",
        "quality_info": "सुरक्षित उपभोग के लिए पानी की गुणवत्ता आवश्यक है। मैं आपके क्षेत्र के लिए भूजल गुणवत्ता पैरामीटर, संदूषण स्तर और उपचार सिफारिशों के बारे में जानकारी प्रदान कर सकता हूं।",
        "default": "मैं समझता हूं कि आप भूजल संबंधी जानकारी चाह रहे हैं। आप मुझसे जल स्तर, गुणवत्ता, वर्षा प्रभाव, बोरिंग स्थान या कोई अन्य भूजल प्रश्न पूछ सकते हैं। मैं विशेष रूप से आपकी कैसे सहायता कर सकता हूं?"
      }
    }
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en', // default language
    fallbackLng: 'en',
    keySeparator: '.',
    interpolation: {
      escapeValue: false // react already does escaping
    },
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      lookupLocalStorage: 'jalbuddy_language',
      caches: ['localStorage']
    }
  });

export default i18n;