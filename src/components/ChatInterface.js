import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Send, Volume2, VolumeX } from 'lucide-react';
import MessageBubble from './MessageBubble';
import LanguageToggle from './LanguageToggle';
import TypingIndicator from './TypingIndicator';
import QuickActions from './QuickActions';
import LoadingSkeleton from './LoadingSkeleton';
import JalBuddyLogo from './JalBuddyLogo';
import { demoIntents } from '../utils/demoData';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState(() => {
    const storedMessages = localStorage.getItem('messages');
    return storedMessages ? JSON.parse(storedMessages) : [];
  });
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [language, setLanguage] = useState('en');
  const [isTyping, setIsTyping] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);
  const [showQuickActions, setShowQuickActions] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  // Initialize welcome message
  useEffect(() => {
    const timer = setTimeout(() => {
      const welcomeText = language === 'hi' 
        ? "नमस्ते! मैं जलबडी हूँ, भूजल जानकारी के लिए आपका AI सहायक। आज मैं आपकी कैसे मदद कर सकता हूँ? 🌊"
        : "Hello! I'm JalBuddy, your AI assistant for groundwater information. How can I help you today? 🌊";
      
      const welcomeMessage = {
        id: 1,
        text: welcomeText,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages([welcomeMessage]);
      setShowWelcome(false);
      setShowQuickActions(true);
      
      if (voiceEnabled) {
        setTimeout(() => {
          speakText(welcomeMessage.text);
        }, 800);
      }
    }, 1500);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = language === 'hi' ? 'hi-IN' : 'en-US';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputText(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = () => {
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, [language]);

  useEffect(() => {
    localStorage.setItem('messages', JSON.stringify(messages));
  }, [messages]);

  const handleSendMessage = () => {
    if (inputText.trim() === '' || isTyping) return;

    const userMessageText = inputText;
    const newMessage = {
      id: Date.now(),
      text: userMessageText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setIsTyping(true);
    
    // Simulate bot thinking time (1.5-2.5 seconds)
    const thinkingTime = 1500 + Math.random() * 1000;
    
    setTimeout(() => {
      const botResponse = generateBotResponse(userMessageText);
      const botMessage = {
        id: Date.now() + 1,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
      
      // Text-to-speech for bot response
      if (voiceEnabled) {
        setTimeout(() => {
          speakText(botResponse);
        }, 300);
      }
    }, thinkingTime);
  };

  const handleQuickAction = (actionKey) => {
    const intentData = demoIntents[actionKey];
    const langData = intentData[language];
    
    // Add user message
    const userMessage = {
      id: Date.now(),
      text: langData.userQuery,
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    setShowQuickActions(false);
    
    // Show bot response with data card after delay
    setTimeout(() => {
      const botMessage = {
        id: Date.now() + 1,
        text: `${language === 'hi' ? 'यहाँ आपके लिए जानकारी है:' : 'Here\'s the information you requested:'}`,
        sender: 'bot',
        timestamp: new Date(),
        dataCard: {
          title: langData.title,
          summary: langData.summary,
          details: langData.details,
          suggestion: langData.suggestion,
          color: getColorForIntent(actionKey)
        }
      };
      
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
      
      if (voiceEnabled) {
        setTimeout(() => {
          speakText(botMessage.text);
        }, 300);
      }
    }, 2000 + Math.random() * 1000);
  };
  
  const getColorForIntent = (intent) => {
    const colors = {
      groundwater: '#3498db',
      rainfall: '#2ecc71',
      boring: '#e67e22',
      quality: '#9b59b6',
      gec: '#e74c3c',
      dwlr: '#1abc9c'
    };
    return colors[intent] || '#3498db';
  };

  const generateBotResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('भूजल') || lowerMessage.includes('groundwater') || lowerMessage.includes('water level')) {
      return language === 'hi' 
        ? "मैं आपकी भूजल जानकारी में मदद कर सकता हूँ! क्या आप किसी विशिष्ट क्षेत्र में जल स्तर, गुणवत्ता या उपलब्धता के बारे में डेटा चाहते हैं? कृपया अपना स्थान या जिला बताएं।"
        : "I can help you with groundwater information! Are you looking for data about water levels, quality, or availability in a specific area? Please specify your location or district.";
    } else if (lowerMessage.includes('वर्षा') || lowerMessage.includes('मानसून') || lowerMessage.includes('rainfall') || lowerMessage.includes('monsoon')) {
      return language === 'hi'
        ? "वर्षा डेटा भूजल रिचार्ज के लिए महत्वपूर्ण है। मैं मौसमी पैटर्न और भूजल स्तर पर उनके प्रभाव के बारे में जानकारी प्रदान कर सकता हूँ। आप किस क्षेत्र में रुचि रखते हैं?"
        : "Rainfall data is crucial for groundwater recharge. I can provide information about seasonal patterns and their impact on groundwater levels. Which region are you interested in?";
    } else if (lowerMessage.includes('बोरिंग') || lowerMessage.includes('boring') || lowerMessage.includes('drilling')) {
      return language === 'hi'
        ? "बोरिंग/ड्रिलिंग जानकारी के लिए, मैं भूजल डेटा, भूवैज्ञानिक सर्वेक्षण और आपके क्षेत्र में सफलता दर के आधार पर इष्टतम स्थानों पर मार्गदर्शन कर सकता हूँ। आपका स्थान क्या है?"
        : "For boring/drilling information, I can guide you on optimal locations based on groundwater data, geological surveys, and success rates in your area. What's your location?";
    } else if (lowerMessage.includes('गुणवत्ता') || lowerMessage.includes('quality') || lowerMessage.includes('contamination')) {
      return language === 'hi'
        ? "पानी की गुणवत्ता सुरक्षित उपभोग के लिए आवश्यक है। मैं आपके क्षेत्र के लिए भूजल गुणवत्ता पैरामीटर, दूषण स्तर और उपचार सिफारिशों के बारे में जानकारी प्रदान कर सकता हूँ।"
        : "Water quality is essential for safe consumption. I can provide information about groundwater quality parameters, contamination levels, and treatment recommendations for your area.";
    } else {
      return language === 'hi'
        ? "मैं समझता हूँ कि आप भूजल संबंधी जानकारी चाह रहे हैं। आप मुझसे जल स्तर, गुणवत्ता, वर्षा प्रभाव, बोरिंग स्थान या कोई अन्य भूजल प्रश्न पूछ सकते हैं। मैं विशेष रूप से आपकी कैसे सहायता कर सकता हूँ?"
        : "I understand you're looking for groundwater-related information. You can ask me about water levels, quality, rainfall impact, boring locations, or any other groundwater queries. How specifically can I assist you?";
    }
  };

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language === 'hi' ? 'hi-IN' : 'en-US';
      utterance.rate = 0.9;
      utterance.pitch = 1;
      window.speechSynthesis.speak(utterance);
    }
  };

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      if (recognitionRef.current) {
        recognitionRef.current.start();
        setIsListening(true);
      } else {
        alert('Speech recognition not supported in this browser');
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-interface" role="main" aria-label="JalBuddy Chat Interface">
      <div className="chat-header" role="banner">
        <div className="header-left">
          <JalBuddyLogo />
          <h1>JalBuddy AI Assistant</h1>
          <span className="subtitle">
            {language === 'hi' ? 'केंद्रीय भूजल बोर्ड | भारत सरकार' : 'Central Ground Water Board | Government of India'}
          </span>
        </div>
        <div className="header-right">
          <button
            className={`voice-toggle ${voiceEnabled ? 'enabled' : ''}`}
            onClick={() => setVoiceEnabled(!voiceEnabled)}
            title={voiceEnabled ? 'Disable voice output' : 'Enable voice output'}
            aria-label={voiceEnabled ? 'Disable voice output' : 'Enable voice output'}
            aria-pressed={voiceEnabled}
          >
            {voiceEnabled ? <Volume2 size={16} /> : <VolumeX size={16} />}
          </button>
          <LanguageToggle language={language} onLanguageChange={setLanguage} />
        </div>
      </div>

      <div className="messages-container" role="log" aria-live="polite" aria-label="Chat messages">
        {isLoading ? (
          <LoadingSkeleton />
        ) : (
          <>
            {showWelcome && (
              <div className="welcome-animation" role="status" aria-label="Welcome animation">
                <div className="welcome-pulse"></div>
                <div className="welcome-text">Welcome to JalBuddy! 🌊</div>
              </div>
            )}
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {showQuickActions && (
              <QuickActions 
                language={language} 
                onActionClick={handleQuickAction} 
                isVisible={showQuickActions} 
              />
            )}
            {isTyping && <TypingIndicator />}
            {error && (
              <div className="error-message" role="alert" aria-live="assertive">
                {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <div className="input-container" role="region" aria-label="Message input">
        <div className="input-wrapper">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={language === 'hi' ? 'यहाँ अपना प्रश्न लिखें...' : 'Type your groundwater query here...'}
            rows={1}
            className="message-input"
            aria-label={language === 'hi' ? 'संदेश इनपुट' : 'Message input'}
            aria-describedby="input-help"
          />
          <div id="input-help" className="sr-only">
            {language === 'hi' 
              ? 'अपना भूजल प्रश्न टाइप करें और Enter दबाएं या Send बटन पर क्लिक करें'
              : 'Type your groundwater question and press Enter or click Send button'
            }
          </div>
          <div className="input-actions">
            <div className="mic-container">
              <button
                className={`mic-button ${isListening ? 'listening' : ''}`}
                onClick={toggleListening}
                title={isListening ? 'Stop recording' : 'Start voice input'}
                aria-label={isListening ? 'Stop voice recording' : 'Start voice input'}
                aria-pressed={isListening}
              >
                {isListening ? <MicOff size={20} /> : <Mic size={20} />}
              </button>
              {isListening && (
                <div className="voice-waveform" aria-hidden="true">
                  <div className="wave-bar"></div>
                  <div className="wave-bar"></div>
                  <div className="wave-bar"></div>
                  <div className="wave-bar"></div>
                  <div className="wave-bar"></div>
                </div>
              )}
            </div>
            <button
              className="send-button"
              onClick={handleSendMessage}
              disabled={inputText.trim() === '' || isTyping}
              title="Send message"
              aria-label="Send message"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;