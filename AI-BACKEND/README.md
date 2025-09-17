# jalBuddy AI Backend

**AI-powered Groundwater Consultation System for Smart India Hackathon 2025**

## 🌟 Features

- **Intelligent Query Processing** - RAG-based groundwater consultation
- **Multilingual Support** - Hindi and English processing
- **INGRES Integration** - Real-time groundwater data access
- **Voice Processing** - Speech-to-text and text-to-speech
- **Confidence Scoring** - Transparent AI reliability metrics
- **RESTful API** - Easy frontend integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Setup environment:**
```bash
python setup.py
```

2. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

3. **Run the server:**
```bash
python main.py
```

4. **Access the API:**
- Server: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## 📚 API Endpoints

### Chat Endpoints
- `POST /api/chat/query` - Process groundwater queries
- `GET /api/chat/examples` - Get example queries
- `GET /api/chat/stats` - System statistics

### Voice Endpoints
- `POST /api/voice/process` - Process voice queries
- `GET /api/voice/supported-languages` - Supported languages

### INGRES Data
- `GET /api/ingres/data/{location}` - Get groundwater data
- `GET /api/ingres/locations` - Available locations
- `GET /api/ingres/alerts/{location}` - Groundwater alerts

### Health & Monitoring
- `GET /api/health` - System health check
- `GET /` - API information

## 🧪 Testing the API

### Text Query Example
```bash
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "भूजल स्तर कैसे चेक करें?",
    "language": "hi",
    "user_id": "test_user"
  }'
```

---

**jalBuddy** - Making groundwater information accessible to everyone! 🌊💧
