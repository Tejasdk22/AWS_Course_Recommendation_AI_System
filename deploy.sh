#!/bin/bash

echo "🚀 AWS Career Guidance AI System Deployment"
echo "============================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run:"
    echo "   aws configure"
    exit 1
fi

echo "✅ AWS CLI and credentials verified"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements_aws.txt

# Run deployment
echo "🚀 Starting deployment..."
python deploy_to_aws.py

echo "🎉 Deployment script completed!"

