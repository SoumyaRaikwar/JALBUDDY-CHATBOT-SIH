# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**JalBuddy** is an AI-powered Progressive Web App (PWA) chatbot designed for Smart India Hackathon 2025, providing groundwater information assistance to farmers, officials, and rural communities in India. The project consists of a React frontend with advanced UI/UX features and a Python FastAPI backend with AI/ML capabilities.

## Architecture

This is a **full-stack web application** with the following structure:

### Frontend (React PWA)
- **Framework**: React 19+ with modern hooks
- **Type**: Progressive Web App with service workers
- **UI Features**: Glass-morphism design, voice input/output, bilingual support (English/Hindi)
- **Key Components**: 
  - `ChatInterface.js` - Main chat component with typing indicators and voice features
  - `QuickActions.js` - Demo feature buttons for presentation
  - `DataCard.js` - Information display cards
  - `demoData.js` - Structured demo data for 6 groundwater features

### Backend (FastAPI AI Service)
- **Framework**: FastAPI with async/await patterns
- **AI Stack**: RAG-based system with transformers, sentence-transformers, GPT4All
- **Voice Processing**: OpenAI Whisper for STT, TTS for text-to-speech
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Architecture Pattern**: Service-oriented with dependency injection

### Key Integration Points
- The frontend communicates with backend via RESTful API endpoints
- Voice processing flows: Browser Speech API → Backend Whisper → AI Service → TTS response
- Bilingual support spans both frontend UI strings and backend AI responses
- Demo mode uses structured data (`demoData.js`) for presentation features

## Development Commands

### Frontend Development
```bash
# Navigate to frontend directory
cd FRONTEND

# Install dependencies (uses legacy peer deps for React 19 compatibility)
npm install --legacy-peer-deps

# Start development server
npm start
# Runs on http://localhost:3000

# Build for production
npm run build

# Run tests
npm run test
```

### Backend Development
```bash
# Navigate to backend directory
cd AI-BACKEND

# Setup Python environment and install dependencies
python setup.py
# This creates venv and installs all requirements

# Activate virtual environment (Windows)
venv\Scripts\activate
# Unix/macOS: source venv/bin/activate

# Start development server
python main.py
# Runs on http://localhost:8000
# API docs: http://localhost:8000/docs

# Alternative quick setup
python setup_simple.py

# Install individual dependencies
pip install -r requirements.txt
```

### Full Stack Development
```bash
# Start both services simultaneously (in separate terminals)
# Terminal 1 - Backend
cd AI-BACKEND && python main.py

# Terminal 2 - Frontend  
cd FRONTEND && npm start
```

### Testing and Validation
```bash
# Backend API health check
curl http://localhost:8000/api/health

# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "भूजल स्तर कैसे चेक करें?", "language": "hi"}'

# Frontend PWA testing
# Open http://localhost:3000 in Chrome/Edge for full feature support
```

## Code Patterns and Conventions

### Frontend Patterns
- **State Management**: React hooks with localStorage persistence for messages
- **Internationalization**: i18next with browser language detection
- **Component Structure**: Functional components with custom hooks
- **Styling**: CSS modules with glass-morphism design system
- **Voice Integration**: Web Speech API with fallback handling

### Backend Patterns  
- **Async Processing**: All AI operations use async/await with proper error handling
- **Service Layer**: AI logic encapsulated in `AIService` class with initialization lifecycle
- **Response Structure**: Consistent JSON responses with confidence scores and sources
- **Multilingual AI**: Dynamic response generation based on language parameter
- **Conversation Context**: User conversation history tracking for context-aware responses

### Configuration Management
- **Frontend**: Environment-based configuration via React env variables
- **Backend**: Settings management via `config/settings.py` with environment detection
- **Development**: Both services designed for hot-reload during development

## Important Technical Details

### Voice Features
- **Browser Compatibility**: Voice features work best in Chrome-based browsers
- **Speech Recognition**: Uses browser's Web Speech API with Hindi/English support
- **Text-to-Speech**: Browser-based synthesis with language-specific voices
- **Fallbacks**: Graceful degradation when voice features unavailable

### Bilingual Support
- **UI Localization**: Complete Hindi translation of all interface elements
- **AI Responses**: Backend generates contextually appropriate responses in both languages
- **Voice Support**: Speech recognition and synthesis configured for both English and Hindi
- **Cultural Adaptation**: Response patterns adapted for rural Indian context

### Demo Presentation Features
- **Quick Actions**: 6 predefined demo buttons showcase real INGRES API integration capabilities
- **Data Cards**: Professional information display with color-coded categories
- **Live Simulation**: Realistic response timing and data variations for demos
- **Structured Demo Data**: `demoData.js` contains bilingual demo content for presentations

### PWA Features
- **Offline Capability**: Service worker enables offline functionality
- **Installability**: Web app manifest allows installation on mobile devices
- **Responsive Design**: Mobile-first approach with touch-friendly interactions
- **Performance**: Optimized for rural internet conditions

## Development Workflow

### Adding New Features
1. **Frontend Changes**: Update components in `src/components/`, add CSS styling
2. **Backend Integration**: Add new API endpoints in `api/routes/`
3. **Bilingual Support**: Update both `i18n.js` and backend response generation
4. **Testing**: Test voice features in supported browsers, validate API responses

### Debugging Common Issues
- **Voice not working**: Check browser compatibility, ensure HTTPS in production
- **Legacy peer deps warning**: Expected for React 19 compatibility, use `--legacy-peer-deps`
- **Backend startup fails**: Check Python version (3.8+), virtual environment activation
- **CORS errors**: Backend configured for development CORS, adjust for production

### Adding Demo Content
- **Update `demoData.js`**: Add new intent with bilingual content structure
- **Add Quick Action**: Update `QuickActions.js` with new button
- **Style Integration**: Add color mapping in `getColorForIntent()` function
- **Test Flow**: Verify complete user interaction flow including voice response

## Deployment Considerations

### Frontend Deployment
- Build optimized bundle with `npm run build`
- Serve with HTTPS for PWA and voice features
- Configure service worker caching strategy
- Test PWA installability on mobile devices

### Backend Deployment  
- AI models require GPU acceleration for production performance
- Environment variables needed for API keys and database connections
- Consider containerization for reproducible deployments
- Monitor memory usage for AI model loading

### Integration Points
- INGRES API integration for real groundwater data (currently mocked)
- CGWB data source connections for regulatory compliance
- SMS/notification services for user alerts
- GIS mapping integration for location-based queries

## Smart India Hackathon Context

This project addresses the SIH 2025 problem statement for AI-powered groundwater information systems. Key differentiators:

- **Accessibility**: Voice-first design for rural users with limited digital literacy
- **Cultural Adaptation**: Hindi language support with culturally appropriate responses  
- **Government Integration**: Built for INGRES API and GEC-2015 guideline compliance
- **Practical Applications**: Real-world use cases like boring location guidance and water quality assessment
- **Modern UX**: Glass-morphism design competing with commercial AI assistants

The demo features showcase production-ready capabilities while the underlying architecture supports scaling to real government data integration.