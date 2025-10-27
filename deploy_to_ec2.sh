#!/bin/bash

###############################################################
# AWS Career Guidance AI System - EC2 Deployment Script
###############################################################

set -e

echo "🚀 AWS Career Guidance AI System - EC2 Deployment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
KEY_NAME="${KEY_NAME:-career-guidance-key}"
SECURITY_GROUP_NAME="${SECURITY_GROUP_NAME:-career-guidance-sg}"
INSTANCE_TYPE="${INSTANCE_TYPE:-t3.medium}"
AMI_ID="${AMI_ID:-ami-0c02fb55956c7d316}" # Amazon Linux 2023
REGION="${AWS_REGION:-us-east-1}"

# Check AWS CLI
echo "📋 Checking prerequisites..."
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI first.${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured. Please run 'aws configure'${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

###############################################################
# Step 1: Create Security Group
###############################################################
echo "🔐 Step 1: Creating Security Group..."

# Check if security group already exists
if aws ec2 describe-security-groups --group-names "$SECURITY_GROUP_NAME" --region "$REGION" &> /dev/null; then
    echo "⚠️  Security group '$SECURITY_GROUP_NAME' already exists. Using existing."
    SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --group-names "$SECURITY_GROUP_NAME" --region "$REGION" --query 'SecurityGroups[0].GroupId' --output text)
else
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name "$SECURITY_GROUP_NAME" \
        --description "Security group for Career Guidance AI System" \
        --region "$REGION" \
        --query 'GroupId' \
        --output text)
    
    echo "✅ Security group created: $SECURITY_GROUP_ID"
    
    # Add inbound rules
    aws ec2 authorize-security-group-ingress \
        --group-id "$SECURITY_GROUP_ID" \
        --protocol tcp \
        --port 22 \
        --cidr 0.0.0.0/0 \
        --region "$REGION" \
        --output text &> /dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id "$SECURITY_GROUP_ID" \
        --protocol tcp \
        --port 8001 \
        --cidr 0.0.0.0/0 \
        --region "$REGION" \
        --output text &> /dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id "$SECURITY_GROUP_ID" \
        --protocol tcp \
        --port 8503 \
        --cidr 0.0.0.0/0 \
        --region "$REGION" \
        --output text &> /dev/null || true
    
    echo "✅ Inbound rules configured"
fi

echo ""

###############################################################
# Step 2: Create Key Pair (if needed)
###############################################################
echo "🔑 Step 2: Checking Key Pair..."

if [ ! -f "${KEY_NAME}.pem" ]; then
    if aws ec2 describe-key-pairs --key-names "$KEY_NAME" --region "$REGION" &> /dev/null; then
        echo "⚠️  Key pair '$KEY_NAME' exists in AWS but not locally. Downloading..."
        aws ec2 delete-key-pair --key-name "$KEY_NAME" --region "$REGION" || true
    fi
    
    echo "Creating new key pair..."
    aws ec2 create-key-pair \
        --key-name "$KEY_NAME" \
        --region "$REGION" \
        --query 'KeyMaterial' \
        --output text > "${KEY_NAME}.pem"
    
    chmod 400 "${KEY_NAME}.pem"
    echo -e "${GREEN}✅ Key pair created and saved as ${KEY_NAME}.pem${NC}"
    echo -e "${RED}⚠️  IMPORTANT: Save this key file securely!${NC}"
else
    echo "✅ Key pair file found locally"
fi

echo ""

###############################################################
# Step 3: Launch EC2 Instance
###############################################################
echo "💻 Step 3: Launching EC2 Instance..."

# Create user data script
cat > user_data.sh <<'EOF'
#!/bin/bash
set -e

# Update system
yum update -y

# Install Python 3.9
yum install -y python3.9 python3.9-pip git

# Install required packages
pip3 install --upgrade pip
pip3 install boto3 botocore requests pandas numpy scikit-learn beautifulsoup4 lxml uvicorn fastapi streamlit

# Create application directory
mkdir -p /opt/career-guidance
chmod 777 /opt/career-guidance

# Create startup script
cat > /opt/career-guidance/start_backend.sh <<'INNER_EOF'
#!/bin/bash
cd /opt/career-guidance
source venv/bin/activate || true
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload > /var/log/career-backend.log 2>&1 &
echo $! > /var/run/career-backend.pid
INNER_EOF

cat > /opt/career-guidance/start_streamlit.sh <<'INNER_EOF'
#!/bin/bash
cd /opt/career-guidance
source venv/bin/activate || true
streamlit run streamlit_app_simple.py --server.port 8503 --server.address 0.0.0.0 > /var/log/career-streamlit.log 2>&1 &
echo $! > /var/run/career-streamlit.pid
INNER_EOF

chmod +x /opt/career-guidance/start_backend.sh
chmod +x /opt/career-guidance/start_streamlit.sh

# Enable automatic startup
echo "*/5 * * * * /opt/career-guidance/start_backend.sh" >> /etc/crontab || true
echo "*/5 * * * * /opt/career-guidance/start_streamlit.sh" >> /etc/crontab || true

EOF

# Launch instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_NAME" \
    --security-group-ids "$SECURITY_GROUP_ID" \
    --region "$REGION" \
    --user-data file://user_data.sh \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ EC2 instance launched: $INSTANCE_ID"
echo "⏳ Waiting for instance to be running..."

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID" --region "$REGION"

echo "✅ Instance is now running"
echo ""

###############################################################
# Step 4: Get Instance Information
###############################################################
echo "📊 Step 4: Getting Instance Information..."

# Get public IP
sleep 10
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "✅ Instance Details:"
echo "   Instance ID: $INSTANCE_ID"
echo "   Public IP: $PUBLIC_IP"
echo "   Key File: ${KEY_NAME}.pem"
echo ""

###############################################################
# Step 5: Display Connection Instructions
###############################################################
echo "🎉 EC2 Instance Deployment Complete!"
echo "======================================="
echo ""
echo "📍 Connection Details:"
echo "   SSH Command: ssh -i ${KEY_NAME}.pem ec2-user@$PUBLIC_IP"
echo ""
echo "🚀 Next Steps:"
echo "   1. Wait 2-3 minutes for instance to fully initialize"
echo "   2. Copy your application to the instance:"
echo "      scp -i ${KEY_NAME}.pem -r * ec2-user@$PUBLIC_IP:/opt/career-guidance/"
echo "   3. SSH into the instance:"
echo "      ssh -i ${KEY_NAME}.pem ec2-user@$PUBLIC_IP"
echo "   4. Configure environment:"
echo "      cd /opt/career-guidance"
echo "      python3 -m venv venv"
echo "      source venv/bin/activate"
echo "      pip install -r requirements.txt"
echo "   5. Start the services:"
echo "      ./start_backend.sh"
echo "      ./start_streamlit.sh"
echo ""
echo "📱 Access Your Application:"
echo "   Backend API: http://$PUBLIC_IP:8001"
echo "   Streamlit UI: http://$PUBLIC_IP:8503"
echo ""
echo "💰 Cost Estimate: ~$30-50/month for t3.medium instance"
echo ""

# Save deployment info
cat > ec2_deployment_info.txt <<EOF
Instance ID: $INSTANCE_ID
Public IP: $PUBLIC_IP
Region: $REGION
Security Group: $SECURITY_GROUP_ID
Key Pair: ${KEY_NAME}.pem
Backend URL: http://$PUBLIC_IP:8001
Streamlit URL: http://$PUBLIC_IP:8503
EOF

echo "✅ Deployment information saved to: ec2_deployment_info.txt"
