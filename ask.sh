#!/bin/bash

echo "🎯 UTD Career Guidance AI System - Ask Agent"
echo "============================================="

# Check if virtual environment exists
if [ ! -d "bedrock_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if question provided
if [ $# -eq 0 ]; then
    echo "Usage: ./ask.sh 'Your question here'"
    echo "Example: ./ask.sh 'I want to become a data scientist'"
    exit 1
fi

# Activate environment and ask agent
source bedrock_env/bin/activate && python3 ask_agent.py "$@"
