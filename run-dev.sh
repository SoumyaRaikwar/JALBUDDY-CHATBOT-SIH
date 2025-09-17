#!/bin/bash

# JalBuddy Development Environment Startup Script
# Smart India Hackathon 2025

echo "🌊 Starting JalBuddy - Groundwater Information Assistant"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "🔧 Setting up development environment..."

# Create necessary directories
mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis
mkdir -p data/qdrant

# Set environment variables
export COMPOSE_PROJECT_NAME=jalbuddy
export POSTGRES_PASSWORD=jalbuddy_dev_2025

echo "🐳 Starting Docker containers..."
docker-compose -f docker-compose.dev.yml up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🏥 Checking service health..."

# Check PostgreSQL
if docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U jalbuddy_user -d jalbuddy > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "⚠️  PostgreSQL is starting up..."
fi

# Check Redis
if docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "⚠️  Redis is starting up..."
fi

echo ""
echo "🎉 JalBuddy Development Environment Started!"
echo "=================================================="
echo "📱 Frontend (React PWA):     http://localhost:3000"
echo "🤖 AI Backend (FastAPI):     http://localhost:8000"
echo "📊 API Documentation:        http://localhost:8000/docs"
echo "🗄️  Database (PostgreSQL):   localhost:5432"
echo "🔄 Redis Cache:              localhost:6379"
echo "🔍 Vector DB (Qdrant):       http://localhost:6333"
echo "🌐 Nginx Proxy:              http://localhost:80"
echo "=================================================="
echo ""
echo "📋 Useful Commands:"
echo "  View logs:           docker-compose -f docker-compose.dev.yml logs -f"
echo "  Stop services:       docker-compose -f docker-compose.dev.yml down"
echo "  Restart backend:     docker-compose -f docker-compose.dev.yml restart backend"
echo "  Database shell:      docker-compose -f docker-compose.dev.yml exec postgres psql -U jalbuddy_user -d jalbuddy"
echo ""
echo "🚀 Ready for Smart India Hackathon 2025!"
