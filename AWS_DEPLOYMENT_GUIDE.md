# 🚀 AWS Deployment Guide

## 📋 Prerequisites

### **Required Tools:**
- ✅ **AWS CLI**: Install from https://aws.amazon.com/cli/
- ✅ **Python 3.9+**: For running deployment scripts
- ✅ **AWS Account**: With appropriate permissions
- ✅ **Git**: For version control

### **AWS Permissions Required:**
- Lambda (create, update functions)
- IAM (create roles and policies)
- API Gateway (create REST APIs)
- Bedrock (invoke models)
- CloudWatch Logs (for Lambda logging)

## 🚀 Quick Deployment

### **Option 1: Automated Deployment (Recommended)**
```bash
# Make deployment script executable
chmod +x deploy.sh

# Run automated deployment
./deploy.sh
```

### **Option 2: Manual Deployment**
```bash
# Install dependencies
pip install -r requirements_aws.txt

# Run deployment script
python deploy_to_aws.py
```

## 🔧 Step-by-Step Deployment

### **Step 1: Configure AWS Credentials**
```bash
# Configure AWS CLI
aws configure

# Enter your credentials:
# AWS Access Key ID: [Your Access Key]
# AWS Secret Access Key: [Your Secret Key]
# Default region name: us-east-1
# Default output format: json
```

### **Step 2: Verify AWS Access**
```bash
# Test AWS credentials
aws sts get-caller-identity

# Should return your account information
```

### **Step 3: Deploy to AWS**
```bash
# Run the deployment
python deploy_to_aws.py
```

## 🏗️ What Gets Deployed

### **AWS Resources Created:**

1. **🔐 IAM Role**: `CareerGuidanceLambdaRole`
   - Lambda execution permissions
   - Bedrock model access
   - S3 bucket access
   - CloudWatch Logs access

2. **⚡ Lambda Function**: `career-guidance-orchestrator`
   - Main orchestrator function
   - Coordinates all 4 AI agents
   - 300-second timeout
   - 512MB memory

3. **🌐 API Gateway**: `CareerGuidanceAPI`
   - REST API endpoint
   - POST `/career-guidance` endpoint
   - CORS enabled
   - Regional deployment

4. **📊 CloudWatch Logs**:
   - Automatic logging for Lambda functions
   - Debug and monitoring capabilities

## 📱 API Usage

### **Endpoint:**
```
https://[api-id].execute-api.us-east-1.amazonaws.com/prod/career-guidance
```

### **Request Format:**
```json
{
  "query": "I want to become a data scientist. What should I learn?",
  "sessionId": "unique-session-id"
}
```

### **Response Format:**
```json
{
  "statusCode": 200,
  "body": {
    "query": "user query",
    "unified_response": "AI-generated response",
    "job_market_insights": "job market analysis",
    "course_recommendations": "course suggestions",
    "career_matching_analysis": "career matching",
    "project_suggestions": "project ideas",
    "session_id": "session-id",
    "timestamp": "2025-01-01T00:00:00Z"
  }
}
```

## 🔧 Configuration

### **Environment Variables:**
- `AWS_DEFAULT_REGION`: us-east-1
- `BEDROCK_MODEL_ID`: amazon.titan-text-express-v1

### **Lambda Configuration:**
- **Runtime**: Python 3.9
- **Timeout**: 300 seconds
- **Memory**: 512 MB
- **Handler**: career_guidance_system.lambda_handler

## 🧪 Testing Your Deployment

### **Test API Endpoint:**
```bash
curl -X POST "https://[api-id].execute-api.us-east-1.amazonaws.com/prod/career-guidance" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I want to become a data scientist",
    "sessionId": "test-session"
  }'
```

### **Test with Python:**
```python
import requests

api_url = "https://[api-id].execute-api.us-east-1.amazonaws.com/prod/career-guidance"

response = requests.post(api_url, json={
    "query": "I want to become a data scientist",
    "sessionId": "test-session"
})

print(response.json())
```

## 📊 Monitoring and Debugging

### **CloudWatch Logs:**
- Navigate to AWS CloudWatch Console
- Go to Log Groups
- Find `/aws/lambda/career-guidance-orchestrator`
- View real-time logs

### **Lambda Metrics:**
- Invocations
- Duration
- Errors
- Throttles

### **API Gateway Metrics:**
- Request count
- Latency
- Error rate
- Cache hit rate

## 💰 Cost Estimation

### **Monthly Costs (Estimated):**
- **Lambda**: $0.20 per 1M requests + $0.0000166667 per GB-second
- **API Gateway**: $3.50 per 1M requests
- **Bedrock**: $0.008 per 1K input tokens + $0.024 per 1K output tokens
- **CloudWatch Logs**: $0.50 per GB ingested

### **Example for 1000 requests/month:**
- Lambda: ~$0.20
- API Gateway: ~$0.0035
- Bedrock: ~$5.00
- **Total**: ~$5.20/month

## 🔒 Security Best Practices

### **IAM Permissions:**
- ✅ Least privilege access
- ✅ Separate roles for different functions
- ✅ Regular permission audits

### **API Security:**
- ✅ Input validation
- ✅ Rate limiting (if needed)
- ✅ CORS configuration
- ✅ HTTPS only

### **Data Protection:**
- ✅ No sensitive data in logs
- ✅ Secure credential storage
- ✅ Encryption in transit

## 🚨 Troubleshooting

### **Common Issues:**

1. **Permission Denied:**
   ```bash
   # Check IAM permissions
   aws iam get-role --role-name CareerGuidanceLambdaRole
   ```

2. **Lambda Timeout:**
   - Increase timeout in Lambda configuration
   - Check Bedrock model availability

3. **API Gateway 500 Error:**
   - Check Lambda function logs
   - Verify integration configuration

4. **Bedrock Access Denied:**
   - Enable Bedrock in your AWS account
   - Request access to Titan models

### **Debug Commands:**
```bash
# Check Lambda function
aws lambda get-function --function-name career-guidance-orchestrator

# Check API Gateway
aws apigateway get-rest-apis

# Check logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/career-guidance
```

## 🎯 Next Steps

### **After Successful Deployment:**

1. **Update Streamlit App:**
   - Replace local API URL with AWS API Gateway URL
   - Test the integration

2. **Monitor Performance:**
   - Set up CloudWatch alarms
   - Monitor costs and usage

3. **Scale if Needed:**
   - Increase Lambda memory if needed
   - Add API Gateway caching
   - Consider Lambda provisioned concurrency

4. **Production Hardening:**
   - Add authentication/authorization
   - Implement rate limiting
   - Set up monitoring and alerting

## 📞 Support

### **Getting Help:**
- **AWS Documentation**: https://docs.aws.amazon.com/
- **Lambda Documentation**: https://docs.aws.amazon.com/lambda/
- **API Gateway Documentation**: https://docs.aws.amazon.com/apigateway/
- **Bedrock Documentation**: https://docs.aws.amazon.com/bedrock/

### **Common Resources:**
- AWS Free Tier: https://aws.amazon.com/free/
- Lambda Pricing: https://aws.amazon.com/lambda/pricing/
- API Gateway Pricing: https://aws.amazon.com/api-gateway/pricing/

---

## 🎉 Congratulations!

Your AWS Career Guidance AI System is now deployed to AWS! 

**Your API is live and ready to serve career guidance requests to users worldwide.** 🌍
