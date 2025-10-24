#!/bin/bash

echo "🎯 UTD Career Guidance AI System - AWS Test"
echo "============================================"

# Check if virtual environment exists
if [ ! -d "bedrock_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and run AWS test
echo "🚀 Testing AWS Lambda functions..."
echo ""

source bedrock_env/bin/activate && python3 test_aws_system.py

echo ""
echo "🎉 AWS test complete! Your system is running in AWS!"
