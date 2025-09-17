#!/bin/bash

# JalBuddy Backend Startup Script
echo "🚀 Starting JalBuddy AI Backend Server..."

# Activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run install_dependencies.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with required configuration."
    exit 1
fi

# Start the FastAPI server
echo "🌟 Starting FastAPI server on http://localhost:8000"
echo "📱 Frontend should connect to this backend"
echo "🔧 Debug mode enabled - server will auto-reload on changes"
echo ""
echo "Available endpoints:"
echo "  - GET  /api/health           - Health check"
echo "  - POST /api/chat/query       - Process chat queries"
echo "  - GET  /api/chat/examples    - Get example queries"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

python main.py
