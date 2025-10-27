#!/bin/bash

###############################################################
# Deploy Application to EC2 Instance
###############################################################

set -e

echo "📦 Deploying Application to EC2"
echo "================================"

# Check if deployment info exists
if [ ! -f "ec2_deployment_info.txt" ]; then
    echo "❌ Deployment info not found. Please run deploy_to_ec2.sh first."
    exit 1
fi

# Load deployment info
source ec2_deployment_info.txt

echo "📋 Deployment Info:"
echo "   Instance: $Instance_ID"
echo "   Public IP: $Public_IP"
echo "   Key File: ${KEY_NAME:-career-guidance-key}.pem"
echo ""

# Check if key file exists
KEY_FILE="${KEY_NAME:-career-guidance-key}.pem"
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file not found: $KEY_FILE"
    exit 1
fi

echo "🚀 Copying files to EC2 instance..."
echo ""

# Create deployment package (excluding unnecessary files)
tar -czf deployment.tar.gz \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='frontend/build' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.log' \
    --exclude='*.zip' \
    --exclude='venv' \
    --exclude='bedrock_env' \
    --exclude='.env' \
    --exclude='cache' \
    --exclude='data' \
    --exclude='logs' \
    agents/ backend/ *.py *.txt *.md *.sh *.json .gitignore

# Copy to EC2
echo "📤 Uploading files to EC2..."
scp -i "$KEY_FILE" deployment.tar.gz ec2-user@"$Public_IP":/opt/career-guidance/

echo "📥 Extracting files on EC2..."
ssh -i "$KEY_FILE" ec2-user@"$Public_IP" <<'ENDSSH'
cd /opt/career-guidance
tar -xzf deployment.tar.gz
rm deployment.tar.gz
echo "✅ Files extracted"
ENDSSH

echo "🐍 Installing dependencies..."
ssh -i "$KEY_FILE" ec2-user@"$Public_IP" <<'ENDSSH'
cd /opt/career-guidance

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "✅ Dependencies installed"
ENDSSH

echo "🔧 Setting up services..."
ssh -i "$KEY_FILE" ec2-user@"$Public_IP" <<'ENDSSH'
cd /opt/career-guidance

# Create directories if they don't exist
mkdir -p logs data cache

# Create startup scripts
cat > start_backend.sh <<'BACKEND_EOF'
#!/bin/bash
cd /opt/career-guidance
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload > /var/log/career-backend.log 2>&1 &
echo $! > /var/run/career-backend.pid
echo "Backend started with PID: $!"
BACKEND_EOF

cat > start_streamlit.sh <<'STREAMLIT_EOF'
#!/bin/bash
cd /opt/career-guidance
source venv/bin/activate
streamlit run streamlit_app_simple.py --server.port 8503 --server.address 0.0.0.0 > /var/log/career-streamlit.log 2>&1 &
echo $! > /var/run/career-streamlit.pid
echo "Streamlit started with PID: $!"
STREAMLIT_EOF

chmod +x start_backend.sh
chmod +x start_streamlit.sh

# Kill any existing processes
pkill -f "uvicorn backend.main:app" || true
pkill -f "streamlit run streamlit_app_simple.py" || true

# Wait a bit
sleep 2

# Start services
./start_backend.sh
sleep 3
./start_streamlit.sh

echo "✅ Services started"
ENDSSH

# Clean up local tar file
rm deployment.tar.gz

echo ""
echo "🎉 Application deployed successfully!"
echo ""
echo "📍 Access your application:"
echo "   Backend API: http://$Public_IP:8001"
echo "   Streamlit UI: http://$Public_IP:8503"
echo ""
echo "🔧 To manage services:"
echo "   SSH: ssh -i $KEY_FILE ec2-user@$Public_IP"
echo "   Start: cd /opt/career-guidance && ./start_backend.sh && ./start_streamlit.sh"
echo "   Check logs: tail -f /var/log/career-backend.log"
echo ""
