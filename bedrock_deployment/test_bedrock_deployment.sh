#!/bin/bash

echo "🧪 Testing Bedrock Deployment..."

# Check if service is running
if sudo systemctl is-active --quiet career-streamlit; then
    echo "✅ Streamlit service is running"
else
    echo "❌ Streamlit service is not running"
    sudo systemctl status career-streamlit
    exit 1
fi

# Check if port is open
if sudo netstat -tlnp | grep -q ":8501"; then
    echo "✅ Port 8501 is open"
else
    echo "❌ Port 8501 is not open"
    exit 1
fi

# Test HTTP connection
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8501 | grep -q "200"; then
    echo "✅ HTTP connection successful"
else
    echo "❌ HTTP connection failed"
    exit 1
fi

echo ""
echo "🎉 All tests passed! Bedrock deployment is working!"
echo "🌐 Access your app at: http://107.21.159.25:8501"
