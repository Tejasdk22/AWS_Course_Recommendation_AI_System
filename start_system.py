#!/usr/bin/env python3
"""
Startup script for AWS Career Guidance AI System
This script helps start the system with proper configuration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed."""
    print("🔍 Checking requirements...")
    
    try:
        import boto3
        import fastapi
        import uvicorn
        import requests
        import pandas
        import numpy
        import sklearn
        print("✅ Python dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def setup_environment():
    """Setup environment variables."""
    print("🔧 Setting up environment...")
    
    # Set default environment variables if not set
    env_vars = {
        'AWS_DEFAULT_REGION': 'us-east-1',
        'LOG_LEVEL': 'INFO',
        'MAX_CONCURRENT_REQUESTS': '10',
        'REQUEST_TIMEOUT': '30'
    }
    
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
            print(f"Set {key}={value}")

def start_backend():
    """Start the backend server."""
    print("🚀 Starting backend server...")
    
    backend_dir = Path(__file__).parent / "backend"
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        # Start the backend server
        subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=backend_dir)
        
        print("✅ Backend server started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the frontend server."""
    print("🎨 Starting frontend server...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Start the frontend server
        subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir)
        
        print("✅ Frontend server started on http://localhost:3000")
        return True
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def main():
    """Main startup function."""
    print("🤖 AWS Career Guidance AI System Startup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Start backend
    if not start_backend():
        print("❌ Failed to start backend")
        sys.exit(1)
    
    # Wait a bit for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(3)
    
    # Start frontend
    if not start_frontend():
        print("❌ Failed to start frontend")
        sys.exit(1)
    
    print("\n🎉 System started successfully!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the system")

if __name__ == "__main__":
    try:
        main()
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down system...")
        sys.exit(0)
