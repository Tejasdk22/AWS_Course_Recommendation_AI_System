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
