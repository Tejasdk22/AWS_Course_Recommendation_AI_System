#!/bin/bash

echo "🚀 Starting UTD Career Guidance AI System on Streamlit"
echo "======================================================"

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend is not running. Starting backend..."
    
    # Start backend in background
    cd "$(dirname "$0")"
    python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
    echo $! > /tmp/backend.pid
    echo "📊 Backend started in background (PID: $(cat /tmp/backend.pid))"
    echo "📝 Backend logs: /tmp/backend.log"
    
    # Wait for backend to start
    echo "⏳ Waiting for backend to initialize..."
    sleep 3
fi

# Start Streamlit
echo ""
echo "🎨 Starting Streamlit app..."
echo "📍 Streamlit will be available at: http://localhost:8503"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

cd "$(dirname "$0")"
streamlit run streamlit_app_simple.py --server.port 8503

