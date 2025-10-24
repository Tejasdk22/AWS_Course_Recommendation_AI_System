#!/usr/bin/env python3
"""
Expose local Streamlit app to the internet using ngrok
This creates a public URL that others can access
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok():
    """Install ngrok"""
    print("📦 Installing ngrok...")
    
    # Check if we're on macOS
    if sys.platform == "darwin":
        print("🍎 macOS detected. Installing via Homebrew...")
        try:
            subprocess.run(["brew", "install", "ngrok/ngrok/ngrok"], check=True)
            print("✅ ngrok installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install via Homebrew")
            print("📋 Manual installation:")
            print("1. Go to https://ngrok.com/download")
            print("2. Download ngrok for macOS")
            print("3. Extract and add to PATH")
            return False
    else:
        print("📋 Please install ngrok manually:")
        print("1. Go to https://ngrok.com/download")
        print("2. Download for your OS")
        print("3. Extract and add to PATH")
        return False

def expose_streamlit_app(port=8503):
    """Expose Streamlit app using ngrok"""
    print(f"🌐 Exposing Streamlit app on port {port}...")
    
    try:
        # Start ngrok tunnel
        ngrok_process = subprocess.Popen([
            "ngrok", "http", str(port),
            "--log=stdout"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("⏳ Starting ngrok tunnel...")
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()
                if tunnels.get('tunnels'):
                    public_url = tunnels['tunnels'][0]['public_url']
                    print(f"🎉 Your app is now accessible at:")
                    print(f"🔗 {public_url}")
                    print(f"\n📱 Share this link with anyone!")
                    print(f"💡 The link will work as long as this script is running")
                    return public_url
        except Exception as e:
            print(f"⚠️ Could not get public URL automatically: {e}")
            print("🔍 Check the ngrok web interface at: http://localhost:4040")
        
        return None
        
    except FileNotFoundError:
        print("❌ ngrok not found. Please install it first.")
        return None
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")
        return None

def main():
    """Main function"""
    print("🌐 Streamlit App Public Access")
    print("=" * 40)
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        print("❌ ngrok is not installed")
        if input("Would you like to install it? (y/n): ").lower() == 'y':
            if not install_ngrok():
                return
        else:
            print("📋 Please install ngrok manually and run this script again")
            return
    
    print("✅ ngrok is installed")
    
    # Check if Streamlit is running
    try:
        response = requests.get(f"http://localhost:8503", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit app is running on port 8503")
        else:
            print("⚠️ Streamlit app may not be running on port 8503")
            print("💡 Make sure to start it with: streamlit run streamlit_app_simple.py --server.port 8503")
    except Exception:
        print("❌ Streamlit app is not running")
        print("💡 Start it first with: streamlit run streamlit_app_simple.py --server.port 8503")
        return
    
    # Expose the app
    public_url = expose_streamlit_app()
    
    if public_url:
        print(f"\n🎉 Success! Your app is now public!")
        print(f"🔗 Share this link: {public_url}")
        print(f"\n⏹️  Press Ctrl+C to stop the tunnel")
        
        try:
            # Keep running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n👋 Stopping tunnel...")
            print(f"🔒 Your app is no longer accessible publicly")
    else:
        print("❌ Failed to create public tunnel")

if __name__ == "__main__":
    main()
