#!/bin/bash

# JalBuddy Backend Dependency Installation Script
# Handles installation with fallback options for problematic packages

echo "🚀 Installing JalBuddy AI Backend Dependencies..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Upgrade pip and setuptools first
echo "⬆️ Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install dependencies with specific strategies
echo "📚 Installing core dependencies..."

# Try installing with different strategies
install_with_fallback() {
    local package=$1
    echo "Installing $package..."
    
    # Try normal installation first
    if pip install "$package"; then
        echo "✅ Successfully installed $package"
        return 0
    fi
    
    # Try with no-cache-dir
    echo "🔄 Retrying $package with --no-cache-dir..."
    if pip install --no-cache-dir "$package"; then
        echo "✅ Successfully installed $package (no cache)"
        return 0
    fi
    
    # Try with no-build-isolation
    echo "🔄 Retrying $package with --no-build-isolation..."
    if pip install --no-build-isolation "$package"; then
        echo "✅ Successfully installed $package (no build isolation)"
        return 0
    fi
    
    echo "❌ Failed to install $package"
    return 1
}

# Install packages in order of dependency
echo "🔧 Installing core framework..."
install_with_fallback "fastapi==0.104.1"
install_with_fallback "uvicorn[standard]==0.24.0"
install_with_fallback "pydantic==2.5.0"
install_with_fallback "pydantic-settings==2.1.0"

echo "🤖 Installing AI/ML packages..."
install_with_fallback "torch>=2.2.0"
install_with_fallback "transformers==4.36.0"
install_with_fallback "sentence-transformers==2.2.2"
install_with_fallback "openai==1.3.5"
install_with_fallback "anthropic==0.7.8"

echo "🔍 Installing RAG & Vector Database..."
install_with_fallback "langchain==0.0.354"
install_with_fallback "chromadb==0.4.20"
install_with_fallback "faiss-cpu>=1.8.0"

echo "🎤 Installing voice processing..."
install_with_fallback "openai-whisper>=20231117"
install_with_fallback "librosa==0.10.1"
install_with_fallback "soundfile>=0.12.0"
install_with_fallback "gTTS==2.4.0"
install_with_fallback "pydub==0.25.1"

echo "📄 Installing document processing..."
install_with_fallback "PyPDF2==3.0.1"
install_with_fallback "python-docx==1.1.0"

echo "🗄️ Installing database & caching..."
install_with_fallback "SQLAlchemy==2.0.23"
install_with_fallback "redis==5.0.1"
install_with_fallback "psycopg2-binary==2.9.9"

echo "🛠️ Installing utilities..."
install_with_fallback "python-dotenv==1.0.0"
install_with_fallback "httpx==0.25.2"
install_with_fallback "numpy==1.24.3"
install_with_fallback "pandas>=1.4,<2.0"

echo "✨ Installation complete! Checking installed packages..."
pip list

echo "🎯 Ready to start JalBuddy AI Backend!"
echo "Run: python main.py"
