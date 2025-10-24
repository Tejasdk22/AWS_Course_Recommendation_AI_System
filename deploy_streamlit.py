#!/usr/bin/env python3
"""
Deploy Streamlit app to cloud services
This script helps deploy the Streamlit app to various cloud platforms
"""

import subprocess
import sys
import os
from pathlib import Path

def deploy_to_streamlit_cloud():
    """Deploy to Streamlit Cloud (free)"""
    print("🚀 Deploying to Streamlit Cloud...")
    print("=" * 50)
    
    print("📋 Steps to deploy to Streamlit Cloud:")
    print("1. Push your code to GitHub")
    print("2. Go to https://share.streamlit.io/")
    print("3. Connect your GitHub repository")
    print("4. Set main file to: streamlit_app_simple.py")
    print("5. Deploy!")
    
    print("\n🔗 Your app will be available at:")
    print("https://your-username-streamlit-app.streamlit.app")
    
    return True

def deploy_to_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    print("=" * 50)
    
    # Create Procfile for Heroku
    procfile_content = "web: streamlit run streamlit_app_simple.py --server.port=$PORT --server.address=0.0.0.0"
    
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    print("✅ Created Procfile for Heroku")
    print("\n📋 Next steps:")
    print("1. Install Heroku CLI")
    print("2. Run: heroku create your-app-name")
    print("3. Run: git push heroku main")
    print("4. Your app will be at: https://your-app-name.herokuapp.com")
    
    return True

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    print("=" * 50)
    
    # Create railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "streamlit run streamlit_app_simple.py --server.port=$PORT --server.address=0.0.0.0",
            "healthcheckPath": "/",
            "healthcheckTimeout": 100
        }
    }
    
    import json
    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ Created railway.json")
    print("\n📋 Next steps:")
    print("1. Go to https://railway.app/")
    print("2. Connect your GitHub repository")
    print("3. Deploy!")
    print("4. Your app will be at: https://your-app-name.railway.app")
    
    return True

def create_requirements_for_deployment():
    """Create requirements.txt for deployment"""
    requirements = [
        "streamlit>=1.28.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0"
    ]
    
    with open("requirements.txt", "w") as f:
        for req in requirements:
            f.write(req + "\n")
    
    print("✅ Created requirements.txt for deployment")

def main():
    """Main deployment function"""
    print("🌐 Streamlit App Deployment Options")
    print("=" * 50)
    
    print("Choose deployment option:")
    print("1. Streamlit Cloud (Free, Easy)")
    print("2. Heroku (Free tier available)")
    print("3. Railway (Free tier available)")
    print("4. Create deployment files only")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    # Create requirements file
    create_requirements_for_deployment()
    
    if choice == "1":
        deploy_to_streamlit_cloud()
    elif choice == "2":
        deploy_to_heroku()
    elif choice == "3":
        deploy_to_railway()
    elif choice == "4":
        print("✅ Deployment files created!")
        print("📁 Files created:")
        print("- requirements.txt")
        print("- Procfile (for Heroku)")
        print("- railway.json (for Railway)")
    else:
        print("❌ Invalid choice")
        return
    
    print("\n🎉 Deployment setup complete!")
    print("📚 For detailed instructions, check the DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
