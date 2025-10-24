# AWS Career Guidance AI System - Deployment Guide

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- Node.js 16+
- AWS Account with Bedrock access
- Git

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AWS_Career_Guidance_AI_System

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# AWS Bedrock Configuration
BEDROCK_MODEL_ID=amazon.titan-text-express-v1

# Application Configuration
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
```

### 4. Test the System

```bash
# Run the simple test
python test_system_simple.py

# If all tests pass, start the system
python start_system.py
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Manual Setup

### Backend Setup

```bash
# Start the backend server
cd backend
python main.py
```

### Frontend Setup

```bash
# Start the frontend server
cd frontend
npm start
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path and module structure

2. **AWS Credentials**
   - Set up AWS credentials in your environment
   - Ensure Bedrock access is enabled in your AWS account

3. **Port Conflicts**
   - Backend runs on port 8000
   - Frontend runs on port 3000
   - Change ports in the configuration if needed

4. **TF-IDF Vectorizer Issues**
   - The system now handles empty vocabularies gracefully
   - Check the logs for specific error messages

### Log Files

- System logs: `logs/career_guidance_system.log`
- Agent logs: `logs/{agent_name}.log`
- Data files: `data/` directory

## 📊 System Architecture

### Components

1. **Frontend (React)**
   - Modern React 18 with hooks
   - Tailwind CSS for styling
   - Context API for state management

2. **Backend (FastAPI)**
   - RESTful API endpoints
   - Async processing
   - CORS enabled for frontend

3. **AI Agents**
   - JobMarketAgent: Scrapes job postings
   - CourseCatalogAgent: Analyzes course catalogs
   - CareerMatchingAgent: Matches skills with jobs
   - ProjectAdvisorAgent: Suggests projects

4. **AWS Integration**
   - Bedrock for AI capabilities
   - Claude 3 Sonnet model
   - IAM for security

### Data Flow

1. User submits query through frontend
2. Backend processes query through all agents
3. Agents fetch and analyze data
4. Unified response generated using Bedrock
5. Response sent back to frontend

## 🚀 Production Deployment

### AWS Lambda Deployment

1. **Package the application**
   ```bash
   pip install -r requirements.txt -t .
   zip -r career-guidance-lambda.zip .
   ```

2. **Deploy to Lambda**
   - Upload zip file to AWS Lambda
   - Set handler to `career_guidance_system.lambda_handler`
   - Configure environment variables
   - Set timeout to 5 minutes

### Docker Deployment

```bash
# Build Docker image
docker build -t career-guidance-ai .

# Run container
docker run -p 8000:8000 career-guidance-ai
```

### AWS Amplify Frontend Deployment

```bash
cd frontend
npm run build
amplify publish
```

## 🔒 Security Considerations

1. **AWS IAM**
   - Use least privilege principle
   - Create specific roles for each service
   - Rotate credentials regularly

2. **API Security**
   - Implement rate limiting
   - Add authentication if needed
   - Use HTTPS in production

3. **Data Privacy**
   - Don't store sensitive user data
   - Use encryption in transit and at rest
   - Follow GDPR/privacy regulations

## 📈 Performance Optimization

1. **Caching**
   - Enable response caching
   - Use Redis for session storage
   - Cache agent responses

2. **Scaling**
   - Use AWS Lambda for auto-scaling
   - Implement connection pooling
   - Monitor performance metrics

3. **Monitoring**
   - Set up CloudWatch logs
   - Monitor API response times
   - Track error rates

## 🆘 Support

If you encounter issues:

1. Check the logs in the `logs/` directory
2. Run the test script: `python test_system_simple.py`
3. Verify all dependencies are installed
4. Check AWS credentials and permissions
5. Review the troubleshooting section above

## 📝 License

This project is licensed under the MIT License.
