#!/usr/bin/env python3
"""
Start all services for AWS Career Guidance AI System
This script starts both the backend API and Streamlit app
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_backend():
    """Start the backend API server."""
    print("🚀 Starting Backend API Server...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=Path(__file__).parent)
        
        print("✅ Backend API Server started on http://localhost:8000")
        return backend_process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_streamlit():
    """Start the Streamlit app."""
    print("🎨 Starting Streamlit App...")
    try:
        # Start Streamlit in background
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8502",
            "--server.headless", "true"
        ], cwd=Path(__file__).parent)
        
        print("✅ Streamlit App started on http://localhost:8502")
        return streamlit_process
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return None

def check_services():
    """Check if services are running."""
    import requests
    
    print("🔍 Checking services...")
    
    # Check backend
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is healthy")
        else:
            print("⚠️ Backend API returned non-200 status")
    except Exception as e:
        print(f"❌ Backend API not responding: {e}")
    
    # Check Streamlit
    try:
        response = requests.get("http://localhost:8502", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit App is running")
        else:
            print("⚠️ Streamlit App returned non-200 status")
    except Exception as e:
        print(f"❌ Streamlit App not responding: {e}")

def main():
    """Main function to start all services."""
    print("🤖 AWS Career Guidance AI System - Starting All Services")
    print("=" * 60)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        sys.exit(1)
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Start Streamlit
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit. Exiting.")
        backend_process.terminate()
        sys.exit(1)
    
    # Wait for Streamlit to start
    print("⏳ Waiting for Streamlit to initialize...")
    time.sleep(3)
    
    # Check services
    check_services()
    
    print("\n🎉 All services started successfully!")
    print("📱 Streamlit App: http://localhost:8502")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")
        if backend_process:
            backend_process.terminate()
        if streamlit_process:
            streamlit_process.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main()
