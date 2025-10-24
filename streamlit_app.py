import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="UTD Course Recommendation AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #374151 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #d1d5db;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    .course-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .course-code {
        font-weight: bold;
        color: #1e40af;
        font-size: 1.1rem;
    }
    .course-name {
        font-weight: 600;
        color: #1f2937;
        margin: 0.25rem 0;
    }
    .course-description {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .skills-badge {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .success-message {
        background: #d1fae5;
        border: 1px solid #10b981;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-message {
        background: #fee2e2;
        border: 1px solid #ef4444;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint - use local backend
API_ENDPOINT = "http://localhost:8001/api/career-guidance"

def call_api(query, major, student_type, career_goal):
    """Call the API Gateway endpoint"""
    try:
        payload = {
            "query": query,
            "major": major,
            "studentType": student_type,
            "careerGoal": career_goal
        }
        
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5  # Reduced timeout for faster response
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"HTTP {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Please check your internet connection."
    except Exception as e:
        return None, f"Error: {str(e)}"

def display_course_recommendations(data):
    """Display course recommendations in a nice format"""
    if not data or 'specific_career_analysis' not in data:
        st.error("No course recommendations found in the response.")
        return
    
    career_analysis = data['specific_career_analysis']
    
    # Career Overview
    st.markdown("### 🎯 Career Overview")
    st.markdown(f"**{career_analysis.get('career_title', 'N/A')}**")
    st.markdown(career_analysis.get('career_description', 'No description available'))
    
    # Market Analysis
    if 'market_analysis' in career_analysis:
        st.markdown("### 📊 Market Analysis")
        market = career_analysis['market_analysis']
        if 'job_market_summary' in market:
            summary = market['job_market_summary']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Opportunities", summary.get('total_opportunities', 'N/A'))
            with col2:
                st.metric("Growth Prospect", summary.get('growth_prospect', 'N/A'))
            with col3:
                st.metric("Average Salary", summary.get('average_salary', 'N/A'))
            with col4:
                st.metric("Top Skills", ", ".join(summary.get('top_skills_demanded', [])[:3]))
    
    # Course Recommendations
    if 'course_recommendations' in career_analysis:
        st.markdown("### 📚 Course Recommendations")
        courses = career_analysis['course_recommendations']
        
        # Core Courses
        if 'core_courses' in courses and courses['core_courses']:
            st.markdown("#### 🔥 Core Courses")
            for course in courses['core_courses']:
                with st.container():
                    st.markdown(f"""
                    <div class="course-card">
                        <div class="course-code">{course.get('code', 'N/A')}</div>
                        <div class="course-name">{course.get('name', 'N/A')}</div>
                        <div class="course-description">{course.get('description', 'No description available')}</div>
                        <div style="margin-top: 0.5rem;">
                            <strong>Credits:</strong> {course.get('credits', 'N/A')} | 
                            <strong>Relevance:</strong> {course.get('career_relevance', 'N/A')}
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <strong>Skills:</strong> 
                            {', '.join([f'<span class="skills-badge">{skill}</span>' for skill in course.get('skills_taught', [])])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Elective Courses
        if 'elective_courses' in courses and courses['elective_courses']:
            st.markdown("#### ⚡ Elective Courses")
            for course in courses['elective_courses']:
                with st.container():
                    st.markdown(f"""
                    <div class="course-card">
                        <div class="course-code">{course.get('code', 'N/A')}</div>
                        <div class="course-name">{course.get('name', 'N/A')}</div>
                        <div class="course-description">{course.get('description', 'No description available')}</div>
                        <div style="margin-top: 0.5rem;">
                            <strong>Credits:</strong> {course.get('credits', 'N/A')} | 
                            <strong>Relevance:</strong> {course.get('career_relevance', 'N/A')}
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <strong>Skills:</strong> 
                            {', '.join([f'<span class="skills-badge">{skill}</span>' for skill in course.get('skills_taught', [])])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Skill Development Path
    if 'skill_development_path' in career_analysis:
        st.markdown("### 🛠️ Skill Development Path")
        skill_path = career_analysis['skill_development_path']
        for level, skills in skill_path.items():
            st.markdown(f"**{level.title()}:** {', '.join(skills)}")
    
    # Project Recommendations
    if 'project_recommendations' in career_analysis:
        st.markdown("### 🚀 Project Recommendations")
        projects = career_analysis['project_recommendations']
        for level, project_list in projects.items():
            st.markdown(f"**{level.replace('_', ' ').title()}:**")
            for project in project_list:
                st.markdown(f"• {project}")
    
    # Next Steps
    if 'next_steps' in career_analysis:
        st.markdown("### 🎯 Next Steps")
        for i, step in enumerate(career_analysis['next_steps'], 1):
            st.markdown(f"{i}. {step}")

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 UTD Course Recommendation AI</h1>
        <p>Get personalized course recommendations powered by AWS Bedrock AgentCore</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for input
    with st.sidebar:
        st.markdown("### 📝 Your Academic Profile")
        
        major = st.selectbox(
            "Your Major",
            ["Business Analytics", "Computer Science", "Information Technology Management", "Mathematics", "Statistics", "Engineering"],
            index=0
        )
        
        student_type = st.selectbox(
            "Student Type",
            ["Undergraduate", "Graduate"],
            index=1
        )
        
        career_goal = st.selectbox(
            "Career Goal",
            ["Data Scientist", "Data Engineer", "Data Analyst", "ML Engineer", "Business Analyst", "Product Manager", "Consultant"],
            index=1
        )
        
        st.markdown("---")
        st.markdown("### 🚀 Ready to Get Recommendations?")
        
        if st.button("Get Course Recommendations", type="primary", use_container_width=True):
            # Construct query
            query = f"I am a {major} {student_type} student at UTD. I want to become a {career_goal}. What courses should I take?"
            
            # Show loading
            with st.spinner("🤖 AI agents are analyzing your academic path..."):
                result, error = call_api(query, major, student_type, career_goal)
            
            if error:
                st.error(f"❌ Error: {error}")
            else:
                st.success("✅ Course recommendations generated successfully!")
                st.session_state['recommendations'] = result
                st.session_state['query_info'] = {
                    'major': major,
                    'student_type': student_type,
                    'career_goal': career_goal,
                    'query': query
                }
    
    # Main content area
    if 'recommendations' in st.session_state:
        data = st.session_state['recommendations']
        query_info = st.session_state['query_info']
        
        # Display parsed information
        st.markdown("### 📋 Your Profile")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Major", query_info['major'])
        with col2:
            st.metric("Student Type", query_info['student_type'])
        with col3:
            st.metric("Career Goal", query_info['career_goal'])
        
        st.markdown("---")
        
        # Display recommendations
        display_course_recommendations(data)
        
        # Agent coordination info
        if 'agent_coordination' in data:
            st.markdown("---")
            st.markdown("### 🤖 AI Agent Coordination")
            coordination = data['agent_coordination']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agents Involved", coordination.get('agents_involved', 'N/A'))
            with col2:
                st.metric("Processing Time", coordination.get('processing_time', 'N/A'))
            with col3:
                st.metric("Focus", coordination.get('focus', 'N/A'))
    
    else:
        # Welcome message
        st.markdown("""
        ### 👋 Welcome to UTD Course Recommendation AI!
        
        This system uses **AWS Bedrock AgentCore** to provide personalized course recommendations based on:
        
        - 🎯 **Your Career Goals** - What you want to become
        - 📚 **UTD Course Catalog** - Available courses and their skills
        - 📊 **Job Market Data** - Real-time industry requirements
        - 🛠️ **Skill Matching** - AI-powered course-to-career alignment
        
        **How it works:**
        1. Select your major, student type, and career goal
        2. Click "Get Course Recommendations"
        3. AI agents analyze your profile and provide personalized recommendations
        4. Get detailed course information, skills, and career progression
        
        **Ready to start?** Use the sidebar to configure your profile!
        """)
        
        # Show system status
        st.markdown("### 🔧 System Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("✅ API Gateway Connected")
        with col2:
            st.success("✅ AWS Bedrock Ready")
        with col3:
            st.success("✅ AI Agents Active")

if __name__ == "__main__":
    main()
