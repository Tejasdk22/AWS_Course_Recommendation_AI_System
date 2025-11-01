# 🎓 UTD Career Guidance AI System

An intelligent career guidance system powered by AWS services that provides personalized course recommendations, job market insights, and career path analysis for UTD students.

## 🏗️ Architecture

```
User → Streamlit (EC2) → API Gateway → AWS Lambda → Response
                                    ↓
                            Multi-Agent System
                                    ↓
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
            JobMarketAgent  CourseCatalogAgent  CareerMatchingAgent
                                    ↓
                            ProjectAdvisorAgent
```

## 📁 Repository Structure

```
├── agents/                          # Multi-Agent System
│   ├── base_agent.py               # Base agent class
│   ├── job_market_agent.py         # Job market analysis
│   ├── course_catalog_agent.py     # UTD course recommendations
│   ├── career_matching_agent.py    # Career path matching
│   ├── project_advisor_agent.py    # Project suggestions
│   └── bedrock_agent_core.py       # Bedrock integration
│
├── bedrock_deployment/              # Bedrock Deployment Package
│   ├── streamlit_app_bedrock.py    # Bedrock-powered Streamlit app
│   ├── deploy_bedrock.sh           # Deployment script
│   ├── quick_deploy.sh             # Quick deployment
│   └── test_bedrock_deployment.sh  # Testing script
│
├── career_guidance_system.py        # Full Bedrock-powered system
├── standalone_lambda_handler.py     # Current deployed Lambda function
├── streamlit_app_simple.py          # Current Streamlit app (deployed)
├── streamlit_app_bedrock.py         # Bedrock Streamlit app (local)
├── setup_api_gateway.py             # API Gateway configuration
├── test_bedrock_local.py            # Bedrock testing
├── test_working_bedrock.py          # Multi-agent Bedrock testing
├── requirements.txt                 # Python dependencies
├── env.example                      # Environment variables template
└── README.md                        # This file
```

## 🚀 Current Deployment

### **Live System:**
- **Streamlit App**: `http://107.21.159.25:8501`
- **API Gateway**: `https://avirahgh5d.execute-api.us-east-1.amazonaws.com/prod`
- **Lambda Function**: `career-guidance-orchestrator`

### **How It Works:**
1. User selects major, student type, and career goal in Streamlit
2. Streamlit sends HTTP POST request to API Gateway
3. API Gateway routes to AWS Lambda function
4. Lambda runs multi-agent system (hardcoded data)
5. Lambda returns JSON response with recommendations
6. Streamlit displays results to user

## 🤖 Multi-Agent System

### **Agents:**

1. **JobMarketAgent** 📊
   - Analyzes job market trends
   - Provides salary information
   - Identifies required skills

2. **CourseCatalogAgent** 📚
   - Recommends UTD courses
   - Provides course descriptions
   - Categorizes core vs elective courses

3. **CareerMatchingAgent** 🎯
   - Matches skills with career goals
   - Analyzes career fit
   - Suggests skill development paths

4. **ProjectAdvisorAgent** 🚀
   - Suggests hands-on projects
   - Provides portfolio ideas
   - Recommends learning resources

## 🔧 Setup & Installation

### **Prerequisites:**
```bash
# Python 3.9+
python --version

# AWS CLI configured
aws --version
aws configure
```

### **Local Development:**
```bash
# Clone repository
git clone <repository-url>
cd AWS_Career_Guidance_AI_System

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your AWS credentials

# Test Bedrock locally
python test_bedrock_local.py

# Run Streamlit locally
streamlit run streamlit_app_simple.py
```

## 🌐 Deployment

### **Option 1: Current System (Lambda + Hardcoded Data)**
Already deployed and running:
- Fast response (~2-5 seconds)
- Reliable and consistent
- No external dependencies

### **Option 2: Bedrock-Powered System (Lambda + AI)**
For AI-powered responses:

```bash
# Navigate to deployment package
cd bedrock_deployment

# Deploy to EC2
./deploy_bedrock.sh

# Test deployment
./test_bedrock_deployment.sh
```

## 🧪 Testing

### **Test Bedrock Connection:**
```bash
python test_bedrock_local.py
```

### **Test Multi-Agent System:**
```bash
python test_working_bedrock.py
```

### **Test API Gateway:**
```bash
curl -X POST "https://avirahgh5d.execute-api.us-east-1.amazonaws.com/prod/api/career-guidance" \
-H "Content-Type: application/json" \
-d '{
    "query": "I want to become a Data Scientist",
    "major": "Computer Science",
    "studentType": "Graduate",
    "careerGoal": "Data Scientist"
}'
```

## 📊 Current vs Bedrock Comparison

| Feature | Current System | Bedrock System |
|---------|---------------|----------------|
| **Response Time** | 2-5 seconds | 40-60 seconds |
| **Data Source** | Hardcoded | Web scraping + AI |
| **AI Processing** | No | Yes (Amazon Titan) |
| **Personalization** | Template-based | AI-generated |
| **Reliability** | Very high | Moderate |
| **Cost** | Low | Moderate |

## 🔑 Environment Variables

Create a `.env` file:
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Bedrock Configuration
BEDROCK_MODEL_ID=amazon.titan-text-express-v1

# API Configuration
API_ENDPOINT=https://avirahgh5d.execute-api.us-east-1.amazonaws.com/prod
```

## 📚 Documentation

- **Architecture**: `ARCHITECTURE_EXPLANATION.md` - Detailed system architecture
- **Bedrock Deployment**: `BEDROCK_DEPLOYMENT_GUIDE.md` - Guide for deploying Bedrock system

## 🎯 Key Features

- ✅ Multi-agent career guidance system
- ✅ Personalized course recommendations
- ✅ Job market analysis
- ✅ Career path matching
- ✅ Project suggestions
- ✅ Interactive chatbot
- ✅ Serverless architecture (AWS Lambda)
- ✅ Real-time API responses
- ✅ Scalable deployment

## 🛠️ Tech Stack

**Frontend:**
- Streamlit (Python web framework)

**Backend:**
- AWS Lambda (Serverless compute)
- AWS API Gateway (API management)
- AWS Bedrock (AI/ML service)

**Agents:**
- Python asyncio (Async processing)
- aiohttp (HTTP client)
- BeautifulSoup4 (Web scraping)
- scikit-learn (Career matching)

## 🚀 Future Enhancements

- [ ] Deploy Bedrock-powered system to production
- [ ] Add database for storing user preferences
- [ ] Implement scheduled web scraping (daily/weekly)
- [ ] Add user authentication
- [ ] Create admin dashboard
- [ ] Add analytics and tracking

## 📝 License

This project is developed for educational purposes.

## 👥 Contributors

Developed as part of AWS Career Guidance AI System project.

---

**Live System**: `http://107.21.159.25:8501`

**API Endpoint**: `https://avirahgh5d.execute-api.us-east-1.amazonaws.com/prod`