#!/bin/bash

echo "🚀 DEPLOYING UTD CAREER GUIDANCE AI FRONTEND"
echo "============================================================"

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Navigate to frontend directory
cd frontend

echo "📦 Step 1: Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

echo "🔧 Step 2: Building the project..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build the project"
    exit 1
fi

echo "✅ Project built successfully"

echo "📁 Step 3: Build artifacts created in 'build' directory"
echo "   • Static files ready for deployment"
echo "   • Optimized for production"
echo "   • All assets bundled and minified"

echo ""
echo "🎉 FRONTEND BUILD COMPLETED!"
echo "============================================================"
echo "✅ React app built successfully"
echo "✅ Tailwind CSS compiled"
echo "✅ All assets optimized"
echo "✅ Ready for deployment"
echo ""
echo "📋 DEPLOYMENT OPTIONS:"
echo "   1. AWS Amplify (Recommended)"
echo "      • Connect GitHub repository"
echo "      • Auto-deploy on push"
echo "      • CDN distribution"
echo ""
echo "   2. Manual Deployment"
echo "      • Upload 'build' folder to web server"
echo "      • Configure web server for SPA"
echo ""
echo "   3. AWS S3 + CloudFront"
echo "      • Upload to S3 bucket"
echo "      • Configure CloudFront distribution"
echo ""
echo "🔗 NEXT STEPS:"
echo "   1. Update API endpoint in src/context/CareerContext.js"
echo "   2. Deploy to your preferred platform"
echo "   3. Test the complete system"
echo ""
echo "🎯 Your modern, responsive UI is ready for deployment!"
