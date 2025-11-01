# 🏗️ System Architecture - Complete Explanation

## 📋 Table of Contents
1. [Overall Architecture](#overall-architecture)
2. [Course Recommendation Flow](#course-recommendation-flow)
3. [Chatbot Flow](#chatbot-flow)
4. [Agent Details](#agent-details)

---

## 🏛️ Overall Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  ┌──────────────────┐              ┌──────────────────┐       │
│  │  Streamlit App   │              │  React Frontend   │       │
│  │  (Port 8503)    │              │  (Port 3000)      │       │
│  └────────┬─────────┘              └────────┬─────────┘       │
└───────────┼─────────────────────────────────┼─────────────────┘
            │                                 │
            └─────────────┬───────────────────┘
                          │
            ┌─────────────▼─────────────┐
            │    FastAPI Backend       │
            │    (Port 8000)           │
            └─────────────┬─────────────┘
                          │
                          │
        ┌─────────────────┴─────────────────┐
        │   CareerGuidanceSystem            │
        │   (Orchestrator)                   │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───▼───┐       ┌────▼────┐       ┌────▼────┐
    │ Job   │       │ Course  │       │Career   │
    │Market │       │Catalog  │       │Matching │
    │Agent  │       │ Agent   │       │ Agent   │
    └───┬───┘       └────┬────┘       └────┬────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                   ┌──────▼──────┐
                   │ Project     │
                   │ Advisor     │
                   │ Agent       │
                   └──────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ AWS Bedrock│
                    │ (Titan AI) │
                    └────────────┘
```

---

## 🔄 Course Recommendation Flow

### Step-by-Step Process:

#### 1. **User Input** 📝
```
User enters:
- Major: Business Analytics
- Student Type: Graduate
- Career Goal: Data Scientist
```

#### 2. **Streamlit App Processing** 🎨
```python
# In streamlit_app_simple.py
def call_real_api(major, student_type, career_goal):
    query = f"I am a {major} {student_type} student..."
    
    # Sends POST request to backend
    response = requests.post(
        "http://localhost:8000/api/career-guidance",
        json={
            "query": query,
            "major": major,
            "studentType": student_type,
            "careerGoal": career_goal
        }
    )
```

#### 3. **Backend API (FastAPI)** 🚀
```python
# In backend/main.py
@app.post("/api/career-guidance")
async def get_career_guidance(request):
    # Extracts query info
    query = request.get("query")
    major = request.get("major")
    student_type = request.get("studentType")
    
    # Calls orchestrator
    response = career_system.process_query(
        query, 
        major=major, 
        student_type=student_type
    )
```

#### 4. **Orchestrator (CareerGuidanceSystem)** 🎼
```python
# In career_guidance_system.py
async def process_query(self, user_query, major, student_type):
    # Creates session
    session_id = f"session_{datetime.now()}"
    
    # Runs ALL agents concurrently (parallel processing)
    agent_responses = await self._run_agents_concurrently(
        user_query, 
        major=major, 
        student_type=student_type
    )
    
    # Runs 4 agents at the same time:
    # ✅ JobMarketAgent
    # ✅ CourseCatalogAgent  
    # ✅ CareerMatchingAgent
    # ✅ ProjectAdvisorAgent
```

#### 5. **Agent Execution (Concurrent)** ⚡

All 4 agents run in parallel:

**A. JobMarketAgent** 📊
```python
async def run(query):
    # 1. Scrape Indeed.com and LinkedIn
    jobs = scrape_jobs("Data Scientist", "Dallas")
    
    # 2. Extract skills from job descriptions
    skills = extract_skills(jobs)
    # Example: ["Python", "SQL", "Machine Learning", "AWS"]
    
    # 3. Send to AWS Bedrock for analysis
    analysis = bedrock_client.invoke_model(
        inputText=f"Analyze these job skills: {skills}"
    )
    
    # 4. Return insights
    return "High demand for Python and ML skills in DFW"
```

**B. CourseCatalogAgent** 📚
```python
async def run(query, major="Business Analytics", student_type="Graduate"):
    # 1. Check major-specific catalog URL
    catalog_url = major_catalog_mapping[major][student_type]
    # Example: https://catalog.utdallas.edu/2025/graduate/programs/jsom/business-analytics
    
    # 2. Scrape UTD course catalog
    html = fetch_webpage(catalog_url)
    
    # 3. Parse course information
    courses = parse_courses(html)
    # Extracts: course code, title, description, skills
    
    # 4. Filter by major prefix
    # Business Analytics students can only see:
    # - BUAN courses
    # - MIS courses  
    # - OPRE courses
    filtered_courses = filter_by_prefix(courses, ["BUAN", "MIS", "OPRE"])
    
    # 5. Filter by student level
    # Graduate students can only see graduate courses
    graduate_courses = filter_by_level(courses, "graduate")
    
    # 6. Return course list
    return graduate_courses
```

**C. CareerMatchingAgent** 🎯
```python
async def run(query):
    # 1. Get job market skills
    job_skills = get_from_job_market_agent()
    
    # 2. Get course skills
    course_skills = get_from_course_catalog_agent()
    
    # 3. Use TF-IDF to match skills
    vectorizer = TfidfVectorizer()
    job_vector = vectorizer.fit_transform([job_skills])
    course_vector = vectorizer.fit_transform([course_skills])
    
    # 4. Calculate cosine similarity
    similarity = cosine_similarity(job_vector, course_vector)
    
    # 5. Rank courses by relevance
    ranked_courses = rank_by_similarity(similarity)
    
    # 6. Return matching analysis
    return "BUAN 6356 closely matches Data Scientist requirements"
```

**D. ProjectAdvisorAgent** 🛠️
```python
async def run(query):
    # 1. Identify skill gaps
    gaps = identify_skill_gaps(
        job_market_skills,
        current_skills
    )
    
    # 2. Generate project suggestions
    suggestions = []
    for gap in gaps:
        project = generate_project(gap)
        suggestions.append(project)
    
    # 3. Return project recommendations
    return suggestions
    # Example: ["Build an ML model", "Create a dashboard"]
```

#### 6. **Unified Response Generation** 🤝
```python
# After all agents finish
unified_response = await _generate_unified_response(
    user_query, 
    agent_responses
)

# Uses AWS Bedrock to combine all agent outputs
bedrock_response = bedrock_client.invoke_model(
    inputText=f"""
    User Query: {user_query}
    Job Market: {job_market_insights}
    Courses: {course_recommendations}
    Matching: {career_matching_analysis}
    Projects: {project_suggestions}
    
    Create a unified recommendation combining all these insights.
    """
)

# Returns structured response
return {
    "unified_response": "...",
    "job_market_insights": "...",
    "course_recommendations": "...",
    "career_matching_analysis": "...",
    "project_suggestions": "..."
}
```

#### 7. **Response to User** ✅
```python
# Backend sends JSON to Streamlit
# Streamlit displays:
- 📊 Job Market Insights
- 📚 Course Recommendations  
- 🎯 Career Matching Analysis
- 🚀 Project Suggestions
- 💬 Chatbot (for questions)
```

---

## 💬 Chatbot Flow

### How the Chatbot Works:

```
┌─────────────────────────────────────────┐
│         User asks a question           │
└───────────────┬───────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│    Streamlit Chatbot Interface          │
│    (In streamlit_app_simple.py)         │
└───────────────┬───────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│   Check Question Type                    │
│   - Greeting? (Hi, Hello)               │
│   - Professor? (teaching, instructor)   │
│   - General? (anything else)            │
└───────────────┬───────────────────────┘
                │
                ├─► Greeting → Friendly response
                │
                ├─► Professor → UTD links
                │
                └─► General → AWS Bedrock
                            │
                            ▼
                   ┌──────────────────┐
                   │  AWS Bedrock    │
                   │  Titan Model    │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Context-aware    │
                   │ AI Response      │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ Display to User │
                   └──────────────────┘
```

### Detailed Chatbot Process:

#### 1. **User Types Question** 💬
```python
# In streamlit_app_simple.py
user_question = st.text_input("Ask a question...")
```

#### 2. **Question Analysis** 🔍
```python
def generate_chatbot_response(question, data, query_info):
    lower_question = question.lower()
    
    # Check for greetings
    if lower_question in ["hi", "hello", "hey"]:
        return """Hi! 👋 Nice to meet you!
        I'm your UTD Course Advisor..."""
    
    # Check for professor questions
    if "professor" in lower_question:
        return """Visit [UTD Coursebook](...)
        for instructor information"""
    
    # General questions → AWS Bedrock
    # ...
```

#### 3. **AWS Bedrock Processing** 🤖
```python
# Build context for Bedrock
context = f"""
You are a helpful UTD course advisor chatbot. 
A {query_info['student_type']} student in {query_info['major']} 
wants to become a {query_info['career_goal']}. 

Their course recommendations:
{data['unified_response'][:2000]}

Answer their question: {question}

Be concise, helpful, and specific to UTD courses.
"""

# Call AWS Bedrock
response = bedrock_client.invoke_model(
    modelId="amazon.titan-text-express-v1",
    body=json.dumps({
        "inputText": context,
        "textGenerationConfig": {
            "maxTokenCount": 500,
            "temperature": 0.7
        }
    })
)

# Extract response
ai_response = response['body']['results'][0]['outputText']
```

#### 4. **Display Response** 📤
```python
# Add to chat history
st.session_state.chat_history.append({
    "role": "user",
    "content": question
})
st.session_state.chat_history.append({
    "role": "assistant", 
    "content": ai_response
})

# Rerun to show new message
st.experimental_rerun()
```

---

## 🧩 Agent Details

### 1. **JobMarketAgent** 📊
- **Source:** Web scraping (Indeed, LinkedIn)
- **Output:** Job requirements, skills, salary trends
- **AI:** AWS Bedrock for market analysis

### 2. **CourseCatalogAgent** 📚
- **Source:** UTD catalog 2025
- **Output:** Course codes, titles, descriptions, skills
- **Filtering:** Major-specific prefixes, student level
- **Example:** BUAN 6312, BUAN 6320, etc.

### 3. **CareerMatchingAgent** 🎯
- **Input:** Job skills + Course skills
- **Output:** Skill matching scores
- **AI:** TF-IDF + Cosine similarity

### 4. **ProjectAdvisorAgent** 🛠️
- **Input:** Skill gaps analysis
- **Output:** Project suggestions
- **AI:** AWS Bedrock for project ideas

---

## ⏱️ Typical Execution Time

```
Total Time: ~15-30 seconds

JobMarketAgent:     5-10 seconds (web scraping)
CourseCatalogAgent: 3-5 seconds (web scraping)
CareerMatchingAgent: 2-3 seconds (computation)
ProjectAdvisorAgent: 1-2 seconds (Bedrock AI)
Unified Response:   3-5 seconds (Bedrock AI)

Note: All agents run CONCURRENTLY (parallel), not sequential!
```

---

## 🔑 Key Technologies

### Backend:
- **FastAPI** - Python web framework
- **asyncio** - Concurrent processing
- **uvicorn** - ASGI server

### AI:
- **AWS Bedrock** - Amazon Titan models
- **TF-IDF** - Text matching
- **Cosine Similarity** - Course-job matching

### Data Sources:
- **UTD Catalog 2025** - Official course data
- **Indeed.com** - Job postings
- **LinkedIn** - Professional network

---

## 🎯 Summary

**When you request recommendations:**
1. Streamlit sends request → Backend API
2. Orchestrator spawns 4 agents (concurrently)
3. Each agent fetches/scrapes data
4. Agents send results to AWS Bedrock for AI analysis
5. Unified response combines all insights
6. Display recommendations + chatbot ready

**When you chat:**
1. Question type detection (greeting/professor/general)
2. Context building (course data + user profile)
3. AWS Bedrock generates intelligent response
4. Display in chat interface

This architecture ensures **real-time UTD data** and **intelligent AI responses** throughout!
