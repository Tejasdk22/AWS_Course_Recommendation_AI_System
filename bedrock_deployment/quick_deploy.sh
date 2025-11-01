#!/bin/bash

echo "⚡ Quick Bedrock Deployment..."

# Copy files to EC2 directory
sudo cp streamlit_app_bedrock.py /opt/career-guidance/
sudo cp career-streamlit-bedrock.service /etc/systemd/system/career-streamlit.service

# Restart service
sudo systemctl daemon-reload
sudo systemctl restart career-streamlit

echo "✅ Quick deployment complete!"
echo "🌐 App available at: http://107.21.159.25:8501"
