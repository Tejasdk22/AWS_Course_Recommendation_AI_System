import streamlit as st
import requests
import json
import time
import re
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# API Configuration
def get_courses_from_api(major, student_type):
    """Get real UTD courses from the fast course endpoint"""
    try:
        level = "graduate" if student_type.lower() in ["graduate", "masters", "phd"] else "undergraduate"
        
        response = requests.get(
            f"{API_ENDPOINT}/api/courses",
            params={
                "major": major,
                "level": level
            },
            timeout=15  # Fast timeout for course scraping
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('courses', [])
        else:
            st.error(f"Failed to fetch courses: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:
        st.error("Course fetch timed out")
        return []
    except Exception as e:
        st.error(f"Error fetching courses: {e}")
        return []

# Use API Gateway instead of direct EC2
API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://avirahgh5d.execute-api.us-east-1.amazonaws.com/prod')

def call_real_api(major, student_type, career_goal, use_agent_core=False):
    """Call the real backend API for course recommendations"""
    try:
        query = f"I am a {major} {student_type} student at UTD. I want to become a {career_goal}. What courses should I take?"
        
        response = requests.post(
            f"{API_ENDPOINT}/api/career-guidance",
            json={
                "query": query,
                "major": major,
                "studentType": student_type,
                "careerGoal": career_goal,
                "useAgentCore": False # Force use_agent_core to False
            },
            timeout=30  # Reduced timeout since we have fast course data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.warning(f"Backend API temporarily unavailable: {e}")
        return None

# Mock data function removed - now using real UTD course data from API

def _parse_courses_from_unified(unified_text: str):
    """Extract course bullets from the unified response for clearer rendering."""
    core, elective = [], []
    if not unified_text:
        return core, elective
    lines = [l.strip() for l in unified_text.splitlines()]
    section = None
    for line in lines:
        lower = line.lower()
        if lower.startswith("### core courses"):
            section = "core"
            continue
        if lower.startswith("### elective courses"):
            section = "elective"
            continue
        if lower.startswith("### ") and not (lower.startswith("### core courses") or lower.startswith("### elective courses")):
            section = None
            continue
        if section in ("core", "elective"):
            if line.startswith("-") or line.startswith("•"):
                item = line.lstrip("-• ")
                (core if section == "core" else elective).append(item)
    return core, elective

@st.cache_resource
def get_bedrock_client():
    """Initialize AWS Bedrock client"""
    try:
        region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        return boto3.client(
            'bedrock-runtime',
            region_name=region,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    except Exception as e:
        st.error(f"Failed to initialize Bedrock client: {e}")
        return None

def generate_chatbot_response(question, data, query_info):
    """Generate chatbot response using AWS Bedrock"""
    
    # Handle greetings and casual conversation
    lower_question = question.lower().strip()
    
    # Greetings
    if lower_question in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy"]:
        return f"""Hi! 👋 Nice to meet you! 

I'm your UTD Course Advisor, here to help you with your academic journey. 

I see you're a **{query_info['student_type']}** student in **{query_info['major']}** looking to become a **{query_info['career_goal']}**. That's exciting!

How can I help you today? You can ask me about:
• 📚 Course requirements and prerequisites
• 🎯 How specific courses align with your career goals
• ⏰ Academic timeline and scheduling
• 📝 What to focus on in your studies
• 🎓 Or anything else about your UTD courses!

What would you like to know?"""
    
    # Thank you responses
    if "thank" in lower_question or "thanks" in lower_question:
        return "You're very welcome! 😊 Is there anything else about your courses or career path I can help you with?"
    
    # Check if asking about professors
    if "professor" in lower_question or "faculty" in lower_question or "instructor" in lower_question or "teaching" in lower_question:
        return """I don't have access to current instructor schedules for specific courses. Here's how to find this information:

📅 **UTD Course Schedule**
• Visit: [UTD Coursebook](https://coursebook.utdallas.edu/) to search by course code (e.g., BUAN 6345)
• View current semester offerings and assigned instructors
• Check class schedules and availability

📧 **Alternative Methods**
• [UTD Academic Catalog](https://catalog.utdallas.edu/) for course coordinators
• Contact your academic advisor for faculty recommendations
• Visit department websites for [faculty directory](https://www.utdallas.edu/directory/)
• Email department admins for current semester instructors

💡 **Tip**: Instructor assignments often change each semester, so checking the current schedule is the most accurate method.

Would you like help with course prerequisites, scheduling, or registration instead?"""
    
    context = f"""
You are a helpful UTD course advisor chatbot. A {query_info['student_type']} student in {query_info['major']} 
wants to become a {query_info['career_goal']}. Here are their course recommendations:

{data['unified_response'][:2000]}

Answer their question: {question}

Be concise, helpful, and specific to UTD courses and requirements. If you don't know something specific, 
suggest they consult with their academic advisor. Keep responses brief and actionable.
"""
    
    try:
        bedrock_client = get_bedrock_client()
        if not bedrock_client:
            return "Error: AWS Bedrock client not configured. Please check your AWS credentials."
        
        model_id = os.getenv('BEDROCK_MODEL_ID', 'amazon.titan-text-express-v1')
        
        # Use Titan Express model format
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "inputText": context,
                "textGenerationConfig": {
                    "maxTokenCount": 500,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }),
            contentType="application/json"
        )
        
        response_body = json.loads(response['body'].read())
        return response_body.get('results', [{}])[0].get('outputText', 'No response generated')
        
    except ClientError as e:
        return f"Error: Failed to generate response - {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error - {str(e)}"

def display_courses_structured(courses, major, career_goal):
    """Display UTD courses in Core and Elective format as separate lists"""
    if not courses:
        st.info("No courses found.")
        return
    
    # The API now returns exactly 6 core + 6 elective courses
    # First 6 are core, next 6 are elective
    core_courses = courses[:6]
    elective_courses = courses[6:12]
    
    # Display Core Courses as bulleted list
    if core_courses:
        st.markdown("### 🎯 Core Courses (6 Required)")
        for course in core_courses:
            st.markdown(f"- **{course['code']} - {course['name']}**: {course['description'][:150]}...")
    
    # Display Elective Courses as bulleted list
    if elective_courses:
        st.markdown("### 📚 Elective Courses (6 Recommended)")
        for course in elective_courses:
            st.markdown(f"- **{course['code']} - {course['name']}**: {course['description'][:150]}...")

def display_recommendations(data):
    """Display recommendations in a nice format"""
    # Display the unified response which contains everything formatted nicely
    st.markdown(data['unified_response'])

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 UTD Course Recommendation AI</h1>
        <p>Get personalized course recommendations for University of Texas at Dallas students</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for input
    with st.sidebar:
        st.markdown("### 📝 Your Academic Profile")
        
        major = st.selectbox(
            "Your Major",
            [
                "Business Analytics",
                "Computer Science",
                "Management Information Systems",
                "Finance",
                "Marketing", 
                "Accounting",
                "Information Technology and Management",
                "Software Engineering",
                "Electrical Engineering",
                "Cybersecurity",
                "Supply Chain Management",
                "Mathematics",
                "Statistics"
            ],
            index=0
        )
        
        student_type = st.selectbox(
            "Student Type",
            ["Undergraduate", "Graduate", "Doctoral"],
            index=1
        )
        
        career_goal = st.selectbox(
            "Career Goal",
            [
                # Data & Analytics Roles
                "Data Scientist", "Data Engineer", "Data Analyst", "ML Engineer", 
                "Business Analyst", "Business Intelligence Analyst", "Analytics Consultant",
                
                # Software & Engineering Roles
                "Software Engineer", "Full Stack Developer", "DevOps Engineer", "Cloud Architect",
                
                # IT & Management Roles
                "IT Manager", "IT Director", "Technology Consultant", "Systems Architect",
                "Cybersecurity Engineer", "Security Analyst", "Security Architect",
                
                # Business & Management Roles
                "Product Manager", "Project Manager", "Business Consultant", "Operations Manager",
                "Supply Chain Manager", "Procurement Manager",
                
                # Finance & Accounting Roles
                "Financial Analyst", "Investment Analyst", "Corporate Accountant", "Auditor",
                
                # Marketing Roles
                "Marketing Manager", "Digital Marketing Specialist", "Brand Manager", "Marketing Analyst"
            ],
            index=0
        )
        
        # Ready section
        st.markdown("---")
        st.markdown("### 🚀 Ready to Get Recommendations?")
        
        if st.button("Get Course Recommendations", type="primary", use_container_width=True):
            # Get AI-powered course recommendations
            with st.spinner("🤖 AI is analyzing your academic path and recommending courses..."):
                result = call_real_api(major, student_type, career_goal, use_agent_core=False)
                
                if result is None:
                    # If AI API fails, show error
                    st.error("AI recommendations temporarily unavailable. Please try again.")
                    return

            st.success("✅ AI course recommendations generated successfully!")
            st.session_state['recommendations'] = result
            st.session_state['query_info'] = {
                'major': major,
                'student_type': student_type,
                'career_goal': career_goal
            }
        
    # Main content area
    if 'recommendations' in st.session_state:
        data = st.session_state['recommendations']
        query_info = st.session_state['query_info']
        
        # Display profile
        st.markdown("### 📋 Your Profile")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Major", query_info['major'])
        with col2:
            st.metric("Student Type", query_info['student_type'])
        with col3:
            st.metric("Career Goal", query_info['career_goal'])
        
        st.markdown("---")
        
        # Create two-column layout: recommendations on left, chatbot on right
        main_col, chat_col = st.columns([2, 1])
        
        with main_col:
            # Display recommendations
            display_recommendations(data)
        
        with chat_col:
            # Chatbot on the right
            st.markdown("### 💬 Course Advisor")
            st.markdown("Ask me about courses!")
            
            # Initialize chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Display chat history in a scrollable container
            if st.session_state.chat_history:
                chat_height = "400px"
                chat_html = "<div style='border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px; height: " + chat_height + "; overflow-y: auto; background-color: #f9f9f9;'>"
                for message in st.session_state.chat_history:
                    if message["role"] == "user":
                        chat_html += f"<div style='text-align: right; margin-bottom: 10px;'><div style='background-color: #0084ff; color: white; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 85%; font-size: 0.85rem;'>{message['content']}</div></div>"
                    else:
                        chat_html += f"<div style='text-align: left; margin-bottom: 10px;'><div style='background-color: #e4e6eb; color: black; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 85%; font-size: 0.85rem;'>{message['content']}</div></div>"
                chat_html += "</div>"
                st.markdown(chat_html, unsafe_allow_html=True)
            else:
                st.info("👋 Start by asking a question!")
            
            # Text input for new questions
            user_question = st.text_input("Ask a question...", key="chat_input")
            
            ask_button = st.button("Ask", type="primary", use_container_width=True)
            
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.experimental_rerun()
            
            # Handle question submission
            if ask_button and user_question:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                
                # Generate AI response
                with st.spinner("Thinking..."):
                    ai_response = generate_chatbot_response(user_question, data, query_info)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                # Clear input and rerun
                st.experimental_rerun()
        
    else:
        # Welcome message
        st.markdown("""
        ### 👋 Welcome to UTD Course Recommendation AI!
        
        This system provides personalized course recommendations for **University of Texas at Dallas** students based on:
        
        - 🎯 **Your Career Goals** - What you want to become
        - 📚 **UTD Course Catalog** - Real UTD courses and their skills
        - 📊 **Job Market Data** - Industry requirements and trends
        - 🛠️ **Skill Matching** - AI-powered course-to-career alignment
        - 🏫 **UTD Resources** - Campus organizations, faculty, and opportunities
        
        **How it works:**
        1. Select your UTD major, student type, and career goal
        2. Click "Get Course Recommendations"
        3. Get personalized UTD-specific recommendations instantly
        
        **Ready to start?** Use the sidebar to configure your UTD profile!
        """)
        
        # Show system status
        st.markdown("### 🔧 UTD System Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("✅ UTD AI System Ready")
        with col2:
            st.success("✅ UTD Course Database Available")
        with col3:
            st.success("✅ UTD Recommendations Engine Active")

if __name__ == "__main__":
    main()
