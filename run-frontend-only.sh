#!/bin/bash

# JalBuddy Frontend Only - Quick Start Script
# For testing the React PWA without backend dependencies

echo "🌊 Starting JalBuddy Frontend (React PWA)"
echo "========================================="

cd FRONTEND

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install --legacy-peer-deps
fi

echo "🚀 Starting React development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Note: Backend features will show connection errors until backend is running"

npm start
