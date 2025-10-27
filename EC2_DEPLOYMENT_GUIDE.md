# 🚀 EC2 Deployment Guide

Complete guide for deploying the AWS Career Guidance AI System to EC2.

## 📋 Prerequisites

### **Required Tools:**
- ✅ **AWS CLI**: Installed and configured
- ✅ **AWS Account**: With EC2 permissions
- ✅ **SSH Client**: For connecting to EC2
- ✅ **SCP**: For copying files to EC2

### **AWS Permissions Required:**
- EC2 (launch instances, create security groups)
- IAM (create key pairs)
- VPC (if using custom VPC)

## 🚀 Quick Deployment

### **Automated Deployment (Recommended):**
```bash
# Make script executable (already done)
chmod +x deploy_to_ec2.sh

# Run deployment
./deploy_to_ec2.sh
```

The script will:
1. ✅ Create security group with required ports
2. ✅ Create and download key pair
3. ✅ Launch EC2 instance
4. ✅ Configure user data for automatic setup
5. ✅ Display connection information

## 📝 Manual Setup

### **Step 1: Create Security Group**
```bash
# Create security group
aws ec2 create-security-group \
    --group-name career-guidance-sg \
    --description "Security group for Career Guidance AI"

# Add SSH rule
aws ec2 authorize-security-group-ingress \
    --group-name career-guidance-sg \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# Add Backend API rule
aws ec2 authorize-security-group-ingress \
    --group-name career-guidance-sg \
    --protocol tcp \
    --port 8001 \
    --cidr 0.0.0.0/0

# Add Streamlit rule
aws ec2 authorize-security-group-ingress \
    --group-name career-guidance-sg \
    --protocol tcp \
    --port 8503 \
    --cidr 0.0.0.0/0
```

### **Step 2: Create Key Pair**
```bash
# Create key pair
aws ec2 create-key-pair \
    --key-name career-guidance-key \
    --query 'KeyMaterial' \
    --output text > career-guidance-key.pem

# Set permissions
chmod 400 career-guidance-key.pem
```

### **Step 3: Launch EC2 Instance**
```bash
# Launch instance
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --instance-type t3.medium \
    --key-name career-guidance-key \
    --security-groups career-guidance-sg \
    --count 1
```

### **Step 4: Get Instance IP**
```bash
# Get public IP
aws ec2 describe-instances \
    --filters "Name=instance-state-name,Values=running" \
    --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress]' \
    --output table
```

## 📦 Deploying Your Application

### **Option 1: Automated Deployment Script**
```bash
# Use the provided deployment script
./deploy_app_to_ec2.sh
```

### **Option 2: Manual Deployment**

#### **A. Copy Application to EC2**
```bash
# Copy all files to EC2
scp -i career-guidance-key.pem -r * \
    ec2-user@YOUR_EC2_IP:/opt/career-guidance/
```

#### **B. SSH into EC2**
```bash
# Connect to EC2 instance
ssh -i career-guidance-key.pem ec2-user@YOUR_EC2_IP
```

#### **C. Install Dependencies**
```bash
# Update system
sudo yum update -y

# Install Python and dependencies
sudo yum install -y python3.9 python3.9-pip git

# Create virtual environment
cd /opt/career-guidance
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

#### **D. Set Up Environment Variables**
```bash
# Create .env file
nano /opt/career-guidance/.env

# Add your AWS credentials:
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.titan-text-express-v1
```

#### **E. Start Services**
```bash
# Start backend
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8001 &
echo $! > /var/run/career-backend.pid

# Start Streamlit
nohup streamlit run streamlit_app_simple.py --server.port 8503 --server.address 0.0.0.0 &
echo $! > /var/run/career-streamlit.pid

# Check status
ps aux | grep uvicorn
ps aux | grep streamlit
```

## 🔧 Service Management

### **Start Services**
```bash
# Backend
cd /opt/career-guidance
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8001 &

# Streamlit
streamlit run streamlit_app_simple.py --server.port 8503 --server.address 0.0.0.0 &
```

### **Stop Services**
```bash
# Stop backend
kill $(cat /var/run/career-backend.pid)

# Stop Streamlit
kill $(cat /var/run/career-streamlit.pid)
```

### **Check Logs**
```bash
# Backend logs
tail -f /var/log/career-backend.log

# Streamlit logs
tail -f /var/log/career-streamlit.log

# Application logs
tail -f /opt/career-guidance/logs/*.log
```

## 🎯 Auto-Start on Boot

### **Create Systemd Service Files**

#### **Backend Service:**
```bash
sudo nano /etc/systemd/system/career-backend.service
```

Add:
```ini
[Unit]
Description=Career Guidance Backend API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/career-guidance
Environment="PATH=/opt/career-guidance/venv/bin"
ExecStart=/opt/career-guidance/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **Streamlit Service:**
```bash
sudo nano /etc/systemd/system/career-streamlit.service
```

Add:
```ini
[Unit]
Description=Career Guidance Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/career-guidance
Environment="PATH=/opt/career-guidance/venv/bin"
ExecStart=/opt/career-guidance/venv/bin/streamlit run streamlit_app_simple.py --server.port 8503 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **Enable Services:**
```bash
# Enable auto-start
sudo systemctl enable career-backend.service
sudo systemctl enable career-streamlit.service

# Start services
sudo systemctl start career-backend.service
sudo systemctl start career-streamlit.service

# Check status
sudo systemctl status career-backend.service
sudo systemctl status career-streamlit.service
```

## 🧪 Testing Your Deployment

### **Test Backend API:**
```bash
# From your local machine
curl http://YOUR_EC2_IP:8001/health

# Test endpoint
curl -X POST http://YOUR_EC2_IP:8001/api/career-guidance \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I want to become a data scientist",
    "sessionId": "test"
  }'
```

### **Test Streamlit:**
```bash
# Open in browser
open http://YOUR_EC2_IP:8503
```

## 🔍 Troubleshooting

### **Common Issues:**

#### **1. Cannot Connect via SSH**
```bash
# Check security group rules
aws ec2 describe-security-groups --group-names career-guidance-sg

# Check instance state
aws ec2 describe-instances --instance-ids i-xxx
```

#### **2. Services Not Running**
```bash
# Check processes
ps aux | grep uvicorn
ps aux | grep streamlit

# Check logs
tail -f /var/log/career-backend.log
tail -f /var/log/career-streamlit.log
```

#### **3. Port Already in Use**
```bash
# Find process using port
sudo lsof -i :8001
sudo lsof -i :8503

# Kill process
sudo kill -9 PID
```

#### **4. AWS Credentials Error**
```bash
# Check environment variables
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

## 💰 Cost Optimization

### **Instance Type Recommendations:**

| Use Case | Instance Type | Cost/month |
|----------|---------------|------------|
| **Development** | t3.micro | ~$7-10 |
| **Testing** | t3.small | ~$15-20 |
| **Production (Low)** | t3.medium | ~$30-40 |
| **Production (Medium)** | t3.large | ~$60-80 |

### **Cost-Saving Tips:**
1. ✅ Use **Spot Instances** for development (up to 90% savings)
2. ✅ **Stop instance** when not in use
3. ✅ Use **t3.small** or **t3.medium** for most use cases
4. ✅ Enable **auto-scaling** based on CPU usage
5. ✅ Use **Reserved Instances** for predictable workloads

### **Stop/Start Instance:**
```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-xxx

# Start instance
aws ec2 start-instances --instance-ids i-xxx

# Get new IP after restart
aws ec2 describe-instances --instance-ids i-xxx \
    --query 'Reservations[0].Instances[0].PublicIpAddress'
```

## 🔒 Security Best Practices

### **1. Security Group Configuration**
```bash
# Limit SSH access to your IP
aws ec2 authorize-security-group-ingress \
    --group-name career-guidance-sg \
    --protocol tcp \
    --port 22 \
    --cidr YOUR_IP/32
```

### **2. AWS Credentials**
- ✅ Never commit credentials to Git
- ✅ Use IAM roles instead of access keys
- ✅ Rotate credentials regularly
- ✅ Use least privilege principle

### **3. Firewall Rules**
```bash
# Set up firewall on EC2
sudo yum install -y firewalld
sudo systemctl enable firewalld
sudo systemctl start firewalld

# Allow only necessary ports
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --permanent --add-port=8503/tcp
sudo firewall-cmd --reload
```

## 📊 Monitoring

### **CloudWatch Monitoring:**
```bash
# Enable detailed monitoring
aws ec2 monitor-instances --instance-ids i-xxx

# View metrics
# Go to CloudWatch Console → Metrics → EC2
```

### **Application Monitoring:**
```bash
# Check application logs
tail -f /var/log/career-backend.log
tail -f /var/log/career-streamlit.log

# Check system resources
top
df -h
free -m
```

## 🎯 Scaling

### **Auto-Scaling Group:**
For production, set up an Auto-Scaling Group:
1. Create Launch Template
2. Create Auto-Scaling Group
3. Configure scaling policies
4. Set up Application Load Balancer

### **Multiple Instances:**
For high availability, deploy multiple instances:
1. Use the same security group
2. Use Application Load Balancer
3. Configure health checks
4. Set up auto-scaling

## 📞 Support

### **Useful Commands:**
```bash
# Instance status
aws ec2 describe-instances

# Stop instance
aws ec2 stop-instances --instance-ids i-xxx

# Terminate instance
aws ec2 terminate-instances --instance-ids i-xxx

# Create AMI (backup)
aws ec2 create-image --instance-id i-xxx --name career-guidance-backup
```

---

## 🎉 Congratulations!

Your Career Guidance AI System is now deployed on EC2!

**Access your application:**
- 🌐 Backend API: `http://YOUR_EC2_IP:8001`
- 🎨 Streamlit UI: `http://YOUR_EC2_IP:8503`

**Next Steps:**
1. Configure custom domain (optional)
2. Set up SSL certificates
3. Configure monitoring and alerts
4. Set up automated backups
