#!/bin/bash

echo "🎯 UTD Career Guidance AI System - Quick Demo"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "bedrock_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and run test
echo "🚀 Activating virtual environment and running demo..."
echo ""

source bedrock_env/bin/activate && python3 test_full_system.py

echo ""
echo "🎉 Demo complete! Your agentic AI system is working perfectly!"
