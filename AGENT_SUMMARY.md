# 🤖 AWS Career Guidance AI System - Agent Summary

## 🏗️ System Architecture

The AWS Career Guidance AI System is a **multi-agent orchestration platform** that provides personalized career guidance for UTD students. The system consists of **4 specialized AI agents** working together to deliver comprehensive recommendations.

## 🎯 Core Agents Overview

### 1. **JobMarketAgent** 📊
**Purpose**: Analyzes current job market trends and requirements

**How it works**:
- **Web Scraping**: Fetches job postings from Indeed and LinkedIn
- **Data Processing**: Extracts skills, requirements, and salary information
- **Market Analysis**: Identifies trending skills and job market demands
- **Output**: JSON file with job market insights and skill requirements

**Key Features**:
- Real-time job market data collection
- Skill extraction and categorization
- Salary trend analysis
- Industry demand forecasting

**Technologies Used**:
- BeautifulSoup for web scraping
- AWS Bedrock for AI analysis
- JSON for data storage

---

### 2. **CourseCatalogAgent** 📚
**Purpose**: Crawls and analyzes UTD course catalog

**How it works**:
- **Web Crawling**: Scrapes UTD course catalog (undergraduate and graduate)
- **Course Extraction**: Parses course codes, descriptions, and prerequisites
- **Skill Mapping**: Identifies skills taught in each course
- **Output**: JSON file with comprehensive course information

**Key Features**:
- UTD-specific course data
- Skill-to-course mapping
- Prerequisite analysis
- Course difficulty assessment

**Technologies Used**:
- BeautifulSoup for web scraping
- AWS Bedrock for content analysis
- JSON for structured data storage

---

### 3. **CareerMatchingAgent** 🎯
**Purpose**: Matches job market requirements with available courses

**How it works**:
- **Data Integration**: Combines job market and course catalog data
- **TF-IDF Vectorization**: Analyzes skill similarity between jobs and courses
- **Matching Algorithm**: Calculates compatibility scores
- **Recommendation Engine**: Suggests relevant courses for career goals

**Key Features**:
- Advanced skill matching algorithms
- Career path optimization
- Gap analysis (missing skills)
- Personalized course recommendations

**Technologies Used**:
- Scikit-learn for TF-IDF vectorization
- AWS Bedrock for intelligent matching
- JSON for data persistence

---

### 4. **ProjectAdvisorAgent** 🚀
**Purpose**: Suggests hands-on projects based on skill gaps

**How it works**:
- **Skill Gap Analysis**: Identifies missing skills from career goals
- **Project Generation**: Creates project ideas to fill skill gaps
- **Difficulty Progression**: Suggests beginner to advanced projects
- **Resource Recommendations**: Provides learning resources and tools

**Key Features**:
- Personalized project suggestions
- Skill-based project categorization
- Learning path recommendations
- Portfolio building guidance

**Technologies Used**:
- AWS Bedrock for project generation
- JSON for project data storage
- Integration with career matching data

---

## 🔄 Agent Orchestration

### **Concurrent Execution**
All agents run **simultaneously** for maximum efficiency:
```python
# All agents execute in parallel
job_market_task = asyncio.create_task(job_market_agent.run())
course_catalog_task = asyncio.create_task(course_catalog_agent.run())
career_matching_task = asyncio.create_task(career_matching_agent.run())
project_advisor_task = asyncio.create_task(project_advisor_agent.run())
```

### **Data Flow**
1. **JobMarketAgent** → Job market data
2. **CourseCatalogAgent** → Course catalog data
3. **CareerMatchingAgent** ← Uses data from agents 1 & 2
4. **ProjectAdvisorAgent** ← Uses data from agent 3
5. **Unified Response** ← Combines all agent outputs

### **Session Management**
- Each query gets a unique session ID
- Agents maintain state across requests
- Data is cached for performance optimization

---

## 🛠️ Technical Implementation

### **Base Agent Architecture**
All agents inherit from `BaseAgent` class:
```python
class BaseAgent:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def run(self):
        # Override in subclasses
        pass
```

### **AWS Bedrock Integration**
- **Model**: Claude 3 Sonnet
- **Purpose**: Natural language processing and analysis
- **Features**: Advanced reasoning and content generation

### **Error Handling**
- **Graceful Degradation**: System continues if individual agents fail
- **Fallback Data**: Uses sample data when external sources fail
- **Comprehensive Logging**: Tracks all agent activities

---

## 📊 Data Outputs

### **JobMarketAgent Output**
```json
{
  "total_jobs": 180,
  "skills_analysis": {...},
  "salary_trends": {...},
  "job_categories": {...}
}
```

### **CourseCatalogAgent Output**
```json
{
  "total_courses": 150,
  "course_details": {...},
  "skill_mapping": {...},
  "prerequisites": {...}
}
```

### **CareerMatchingAgent Output**
```json
{
  "matching_scores": {...},
  "recommended_courses": [...],
  "skill_gaps": [...],
  "career_path": {...}
}
```

### **ProjectAdvisorAgent Output**
```json
{
  "project_suggestions": [...],
  "difficulty_levels": {...},
  "learning_resources": [...],
  "timeline": {...}
}
```

---

## 🎯 Use Cases

### **For UTD Students**
- **Course Selection**: Get personalized course recommendations
- **Career Planning**: Understand job market requirements
- **Skill Development**: Identify and fill skill gaps
- **Project Ideas**: Find hands-on projects to build portfolio

### **For Academic Advisors**
- **Student Guidance**: Provide data-driven career advice
- **Course Planning**: Optimize student academic paths
- **Market Alignment**: Ensure courses meet industry needs

### **For Career Services**
- **Job Market Insights**: Understand current hiring trends
- **Skill Mapping**: Connect academic programs to careers
- **Resource Planning**: Identify areas for program development

---

## 🚀 Performance Features

### **Scalability**
- **Async Processing**: All agents run concurrently
- **Caching**: Results are cached for repeated queries
- **Session Management**: Efficient state handling

### **Reliability**
- **Error Recovery**: System continues if agents fail
- **Data Validation**: Ensures data quality and consistency
- **Monitoring**: Comprehensive logging and health checks

### **Flexibility**
- **Modular Design**: Easy to add new agents
- **Configurable**: Adjustable parameters and settings
- **Extensible**: Simple to add new data sources

---

## 🔧 Configuration

### **Environment Variables**
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
```

### **Agent Settings**
- **Timeout**: 30 seconds per agent
- **Retry Logic**: 3 attempts for failed requests
- **Data Persistence**: JSON file storage

---

## 📈 Future Enhancements

### **Planned Features**
- **Real-time Updates**: Live job market data
- **Machine Learning**: Improved matching algorithms
- **API Integration**: Direct integration with UTD systems
- **Mobile App**: Native mobile application

### **Advanced Capabilities**
- **Predictive Analytics**: Forecast career trends
- **Skill Assessment**: Evaluate current skill levels
- **Mentorship Matching**: Connect students with mentors
- **Industry Partnerships**: Direct company integration

---

## 🎓 UTD-Specific Features

### **Course Integration**
- **Real UTD Courses**: BUAN, MIS, CS, ITSS, MATH, STAT
- **Prerequisite Mapping**: Course dependency analysis
- **Academic Timeline**: Semester-by-semester planning

### **Campus Resources**
- **Faculty Connections**: Professor research areas
- **Student Organizations**: Relevant clubs and societies
- **Career Services**: UTD-specific career resources
- **Internship Programs**: Local company partnerships

This multi-agent system provides a comprehensive, AI-powered career guidance platform specifically tailored for University of Texas at Dallas students, combining real-time job market data with academic course offerings to deliver personalized recommendations.
