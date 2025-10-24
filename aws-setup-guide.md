# AWS Setup Guide for Career Guidance AI System

## 🚀 **Step-by-Step AWS Configuration**

### **Step 1: Create IAM Policy**

1. **Go to AWS Console** → IAM → Policies → Create Policy
2. **Choose JSON tab** and paste the contents of `aws-iam-policy.json`
3. **Name the policy**: `CareerGuidanceAI-BedrockAccess`
4. **Description**: `Policy for Career Guidance AI System to access Bedrock and other AWS services`
5. **Click "Create Policy"**

### **Step 2: Create IAM Role (Recommended)**

1. **Go to AWS Console** → IAM → Roles → Create Role
2. **Select "AWS Service"** → **"EC2"** (for local development)
3. **Attach the policy** you just created: `CareerGuidanceAI-BedrockAccess`
4. **Name the role**: `CareerGuidanceAI-Role`
5. **Description**: `Role for Career Guidance AI System`
6. **Click "Create Role"**

### **Step 3: Create IAM User (Alternative)**

If you prefer using a user instead of a role:

1. **Go to AWS Console** → IAM → Users → Create User
2. **Username**: `career-guidance-ai-user`
3. **Attach policies directly**: `CareerGuidanceAI-BedrockAccess`
4. **Create Access Keys** for this user
5. **Download the credentials**

### **Step 4: Enable Bedrock Access**

1. **Go to AWS Console** → Bedrock
2. **Navigate to "Model access"** in the left sidebar
3. **Amazon Titan models are available by default** (no approval needed):
   - amazon.titan-text-express-v1
   - amazon.titan-text-lite-v1
   - amazon.titan-embed-text-v1

### **Step 5: Configure Your Environment**

```bash
# Copy the environment template
cp env.example .env

# Edit with your credentials
nano .env
```

**Fill in your .env file:**
```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# AWS Bedrock Configuration
BEDROCK_MODEL_ID=amazon.titan-text-express-v1
BEDROCK_AGENT_ID=your_bedrock_agent_id
BEDROCK_AGENT_ALIAS_ID=TSTALIASID

# Application Configuration
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
```

### **Step 6: Test Your Configuration**

```bash
# Activate virtual environment
source bedrock_env/bin/activate

# Test AWS connection
python -c "
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
client = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
print('✅ AWS Bedrock client created successfully!')
print(f'Region: {os.getenv(\"AWS_DEFAULT_REGION\", \"us-east-1\")}')
"
```

## 🔧 **Alternative: AWS CLI Configuration**

If you prefer using AWS CLI:

```bash
# Install AWS CLI (if not already installed)
pip install awscli

# Configure AWS CLI
aws configure
# Enter your credentials when prompted

# Test configuration
aws sts get-caller-identity
```

## 📋 **Required Permissions Summary**

Your IAM policy needs these permissions:

- **bedrock:InvokeModel** - To call Claude models
- **bedrock:InvokeModelWithResponseStream** - For streaming responses
- **bedrock:ListFoundationModels** - To list available models
- **logs:CreateLogGroup, logs:PutLogEvents** - For logging
- **s3:GetObject, s3:PutObject** - For data storage (optional)

## ⚠️ **Security Best Practices**

1. **Use least privilege principle** - Only grant necessary permissions
2. **Rotate access keys regularly** - Every 90 days
3. **Use IAM roles when possible** - More secure than access keys
4. **Enable MFA** - For additional security
5. **Monitor usage** - Check CloudTrail logs

## 🧪 **Testing Your Setup**

After configuration, test the system:

```bash
# Run the test script
source bedrock_env/bin/activate
python test_system.py

# Or start the development server
python backend/main.py
```

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **"Access Denied" errors**:
   - Check if Bedrock access is enabled
   - Verify IAM permissions
   - Ensure correct region

2. **"Model not found" errors**:
   - Check model ID format
   - Verify model access in Bedrock console

3. **"Invalid credentials" errors**:
   - Verify AWS credentials
   - Check .env file format
   - Test with `aws sts get-caller-identity`

### **Need Help?**
- Check AWS CloudTrail for detailed error logs
- Verify your IAM policy syntax
- Ensure Bedrock is available in your region
