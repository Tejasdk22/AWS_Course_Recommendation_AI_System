#!/bin/bash

echo "🚀 Deploying Bedrock-Powered Streamlit App..."

# Stop current Streamlit service
sudo systemctl stop career-streamlit

# Copy new app
sudo cp streamlit_app_bedrock.py /opt/career-guidance/

# Update systemd service
sudo cp career-streamlit-bedrock.service /etc/systemd/system/career-streamlit.service

# Reload systemd
sudo systemctl daemon-reload

# Start new service
sudo systemctl start career-streamlit

# Enable service
sudo systemctl enable career-streamlit

# Check status
echo "📊 Service Status:"
sudo systemctl status career-streamlit --no-pager -l

echo ""
echo "🎉 Deployment Complete!"
echo "🌐 Access your app at: http://107.21.159.25:8501"
echo "🤖 Now powered by Amazon Bedrock!"
