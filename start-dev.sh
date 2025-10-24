#!/bin/bash

echo "🚀 STARTING UTD CAREER GUIDANCE AI DEVELOPMENT SERVER"
echo "============================================================"

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Navigate to frontend directory
cd frontend

echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

echo "🌐 Starting development server..."
echo "   • React app will open at http://localhost:3000"
echo "   • Hot reload enabled"
echo "   • Development tools available"
echo ""

npm start
