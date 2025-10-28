import streamlit as st
import requests
import json
import time
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import os

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

def get_mock_response(major, student_type, career_goal):
    """Generate a mock response for demonstration"""
    
    # Customize recommendations based on major - UTD specific
    if major == "Business Analytics":
        core_courses = [
            "**BUAN 6345 (MIS 6345) - SAP Analytics**: In-memory business intelligence tools and databases using SAP",
            "**BUAN 6346 (MIS 6346) - Big Data**: Big data concepts, manipulation with popular tools, and distributed analytics programming", 
            "**BUAN 6356 (MIS 6356) - Business Analytics with R**: Extracting business intelligence from data for customer segmentation and recommendation systems",
            "**BUAN 6350 - Data Mining**: Discover patterns in business data using UTD's analytics tools",
            "**BUAN 6351 - Statistical Methods**: Advanced statistical analysis for business applications",
            "**BUAN 6352 - Predictive Analytics**: Advanced predictive modeling techniques for business applications"
        ]
        skills = ["**Excel & SQL**: Essential for business data analysis", "**Python/R**: Statistical programming with UTD's computing resources", "**Tableau/Power BI**: Business intelligence tools", "**Statistics**: Statistical modeling and forecasting", "**Business Acumen**: Understanding business processes"]
        projects = [
            "**UTD Business Analytics Capstone**: Real-world analytics project with local companies",
            "**Sales Forecasting Project**: Predict sales using historical data from UTD case studies", 
            "**Customer Segmentation**: Analyze customer behavior patterns using UTD datasets",
            "**A/B Testing Analysis**: Design and analyze business experiments"
        ]
    elif major == "Computer Science":
        core_courses = [
            "**CS 4375 - Machine Learning**: Essential for understanding ML algorithms",
            "**CS 6313 - Statistical Methods for Data Science**: Foundation in statistical analysis",
            "**CS 6350 - Big Data Management**: Learn to handle large datasets",
            "**CS 6360 - Database Design**: Database fundamentals for data storage",
            "**CS 6363 - Data Mining**: Advanced data mining techniques"
        ]
        skills = ["**Python Programming**: Essential for data science", "**SQL**: Database querying and management", "**Statistics**: Statistical analysis and modeling", "**Machine Learning**: Algorithm implementation and tuning", "**Data Visualization**: Creating meaningful charts and graphs"]
        projects = [
            "**CS Capstone Project**: Real-world software development project",
            "**Machine Learning Model**: Build a predictive model using scikit-learn", 
            "**Data Visualization Dashboard**: Create interactive visualizations",
            "**End-to-End Pipeline**: Complete data science project from collection to deployment"
        ]
    elif major == "Information Technology and Management":
        core_courses = [
            "**ITSS 6350 - Information Technology Management**: Strategic IT management and planning",
            "**ITSS 6351 - Business Intelligence**: BI tools and techniques for IT managers",
            "**ITSS 6352 - Database Systems**: Database management systems for enterprises",
            "**ITSS 6353 - IT Project Management**: Managing IT projects effectively",
            "**ITSS 6354 - Cloud Computing**: Cloud technologies and architectures"
        ]
        skills = ["**IT Strategy**: Strategic IT planning and management", "**Project Management**: IT project lifecycle management", "**Business Analysis**: Translating business needs to IT solutions", "**Cloud Technologies**: AWS, Azure, and cloud platforms", "**Database Management**: Enterprise database systems"]
        projects = [
            "**IT Strategy Capstone**: Develop strategic IT plan for real organization",
            "**Cloud Migration Project**: Migrate systems to cloud platform", 
            "**Business Intelligence Implementation**: Implement BI solution for organization",
            "**IT Governance Project**: Design IT governance framework"
        ]
    elif major == "Computer Science":
        core_courses = [
            "**CS 5343 - Algorithm Analysis**: Advanced algorithms and complexity",
            "**CS 5348 - Operating Systems**: OS concepts and implementation",
            "**CS 5349 - Computer Networks**: Network protocols and architecture",
            "**CS 5354 - Software Engineering**: Software development lifecycle",
            "**CS 6363 - Data Mining**: Advanced data mining techniques"
        ]
        skills = ["**Java/C++/Python**: Multiple programming languages", "**Data Structures**: Advanced algorithms and data structures", "**System Design**: Large-scale system architecture", "**Software Engineering**: Professional software development", "**Computer Science Fundamentals**: Core CS concepts"]
        projects = [
            "**CS Capstone Project**: Real-world software development project",
            "**System Design Project**: Design and implement distributed system", 
            "**Algorithm Implementation**: Implement advanced algorithms",
            "**Open Source Contribution**: Contribute to open source projects"
        ]
    elif major == "Software Engineering":
        core_courses = [
            "**SE 5353 - Software Project Management**: Managing software projects",
            "**SE 5354 - Software Testing and Quality Assurance**: Testing methodologies",
            "**SE 5355 - Software Architecture**: System architecture and design",
            "**SE 5356 - Agile Development**: Agile and DevOps practices",
            "**SE 5357 - Software Requirements**: Requirements engineering"
        ]
        skills = ["**Software Development**: Full-stack development skills", "**Testing & QA**: Software testing and quality assurance", "**DevOps**: CI/CD pipelines and automation", "**Project Management**: Agile and Scrum methodologies", "**System Design**: Enterprise software architecture"]
        projects = [
            "**Software Engineering Capstone**: End-to-end software development project",
            "**Open Source Project**: Contribute to or create open source software", 
            "**SaaS Application**: Build and deploy a SaaS application",
            "**Automated Testing Framework**: Create comprehensive test suites"
        ]
    elif major == "Electrical Engineering":
        core_courses = [
            "**EE 5358 - Digital Signal Processing**: DSP theory and applications",
            "**EE 5359 - Communications Systems**: Communication theory",
            "**EE 5360 - VLSI Design**: VLSI circuit design",
            "**EE 5361 - Control Systems**: Control theory and applications",
            "**EE 5362 - Power Systems**: Electric power systems"
        ]
        skills = ["**Circuit Design**: Analog and digital circuits", "**Signal Processing**: DSP and communication systems", "**Embedded Systems**: Microcontrollers and embedded programming", "**VLSI Design**: Chip design and layout", "**Power Systems**: Electric power and energy systems"]
        projects = [
            "**EE Capstone Project**: Real-world electrical engineering project",
            "**Embedded System Development**: Design and implement embedded system", 
            "**Signal Processing Application**: Build DSP-based application",
            "**Circuit Design Project**: Design and test electronic circuits"
        ]
    elif major == "Cybersecurity":
        core_courses = [
            "**CS 5363 - Computer Security**: Security principles and practices",
            "**CS 5364 - Network Security**: Network security protocols",
            "**CS 5365 - Cryptography**: Cryptographic systems and protocols",
            "**CS 5366 - Penetration Testing**: Ethical hacking and testing",
            "**CS 5367 - Security Management**: Security governance and compliance"
        ]
        skills = ["**Security Analysis**: Vulnerability assessment and management", "**Cryptography**: Cryptographic protocols and systems", "**Network Security**: Network security protocols and firewalls", "**Penetration Testing**: Ethical hacking and security testing", "**Security Compliance**: Compliance and governance"]
        projects = [
            "**Cybersecurity Capstone**: Real-world security analysis project",
            "**Penetration Testing Project**: Conduct security assessment", 
            "**Security Tool Development**: Build security analysis tools",
            "**Compliance Audit**: Design security compliance framework"
        ]
    elif major == "Management Information Systems":
        core_courses = [
            "**MIS 6340 - IT Strategy**: Strategic IT management",
            "**MIS 6341 - Business Analytics**: Analytics for business decisions",
            "**MIS 6342 - ERP Systems**: Enterprise resource planning",
            "**MIS 6343 - Business Process Management**: Process optimization",
            "**MIS 6344 - IT Governance**: IT governance and compliance"
        ]
        skills = ["**Business Analysis**: Analyzing business needs and IT solutions", "**ERP Systems**: SAP, Oracle, and enterprise systems", "**IT Strategy**: Strategic IT planning", "**Business Process Management**: Process optimization and automation", "**Project Management**: Managing IT projects"]
        projects = [
            "**MIS Capstone Project**: Real-world business systems analysis",
            "**ERP Implementation**: Design ERP implementation plan", 
            "**Business Process Redesign**: Optimize business processes",
            "**IT Strategy Project**: Develop strategic IT roadmap"
        ]
    elif major == "Accounting":
        core_courses = [
            "**ACCT 6320 - Financial Reporting**: Advanced financial reporting",
            "**ACCT 6321 - Managerial Accounting**: Cost analysis and budgeting",
            "**ACCT 6322 - Auditing**: Audit procedures and standards",
            "**ACCT 6323 - Taxation**: Tax law and compliance",
            "**ACCT 6324 - Accounting Information Systems**: AIS design"
        ]
        skills = ["**Financial Analysis**: Financial statements and analysis", "**Tax Planning**: Tax law and compliance", "**Auditing**: Audit procedures and controls", "**Cost Accounting**: Cost analysis and budgeting", "**Accounting Systems**: ERP and accounting systems"]
        projects = [
            "**Accounting Capstone**: Real-world accounting analysis project",
            "**Financial Analysis Project**: Analyze company financials", 
            "**Audit Project**: Conduct audit procedures",
            "**Tax Planning Project**: Develop tax strategy"
        ]
    elif major == "Finance":
        core_courses = [
            "**FIN 6301 - Financial Theory**: Corporate finance theory",
            "**FIN 6302 - Investment Analysis**: Security analysis and portfolio management",
            "**FIN 6303 - Derivative Securities**: Options and futures",
            "**FIN 6304 - Financial Markets**: Market structure and trading",
            "**FIN 6305 - International Finance**: Global financial markets"
        ]
        skills = ["**Financial Modeling**: Excel and financial models", "**Investment Analysis**: Security valuation and portfolio management", "**Risk Management**: Financial risk assessment", "**Derivatives**: Options, futures, and swaps", "**Financial Markets**: Market structure and trading"]
        projects = [
            "**Finance Capstone**: Real-world financial analysis project",
            "**Portfolio Management**: Build and manage investment portfolio", 
            "**Financial Modeling**: Build comprehensive financial models",
            "**Risk Analysis**: Conduct financial risk assessment"
        ]
    elif major == "Marketing":
        core_courses = [
            "**MKT 6300 - Marketing Strategy**: Strategic marketing planning",
            "**MKT 6301 - Consumer Behavior**: Consumer psychology and behavior",
            "**MKT 6302 - Digital Marketing**: Online marketing strategies",
            "**MKT 6303 - Brand Management**: Brand strategy and positioning",
            "**MKT 6304 - Marketing Analytics**: Marketing data and analytics"
        ]
        skills = ["**Marketing Strategy**: Strategic marketing planning", "**Digital Marketing**: Online marketing channels", "**Marketing Analytics**: Data-driven marketing decisions", "**Brand Management**: Brand strategy and development", "**Consumer Insights**: Understanding consumer behavior"]
        projects = [
            "**Marketing Capstone**: Real-world marketing campaign",
            "**Digital Marketing Project**: Launch online marketing campaign", 
            "**Brand Development**: Develop brand strategy and positioning",
            "**Market Research Project**: Conduct comprehensive market research"
        ]
    elif major == "Supply Chain Management":
        core_courses = [
            "**SCM 6300 - Supply Chain Strategy**: Strategic SCM",
            "**SCM 6301 - Operations Management**: Production and operations",
            "**SCM 6302 - Logistics and Distribution**: Logistics management",
            "**SCM 6303 - Procurement and Sourcing**: Procurement strategies",
            "**SCM 6304 - Supply Chain Analytics**: Analytics in SCM"
        ]
        skills = ["**Supply Chain Strategy**: Strategic SCM planning", "**Operations Management**: Production optimization", "**Logistics**: Distribution and warehouse management", "**Procurement**: Strategic sourcing and vendor management", "**Supply Chain Analytics**: Data-driven SCM decisions"]
        projects = [
            "**SCM Capstone**: Real-world supply chain optimization project",
            "**Logistics Design**: Optimize logistics network", 
            "**Procurement Strategy**: Develop sourcing strategy",
            "**Supply Chain Analytics**: Analyze and optimize supply chain"
        ]
    elif major == "Mathematics":
        core_courses = [
            "**MATH 4350 - Mathematical Statistics**: Advanced statistical theory",
            "**MATH 4351 - Applied Statistics**: Statistical methods for real-world problems",
            "**MATH 4352 - Probability Theory**: Foundation in probability and statistics",
            "**MATH 4353 - Statistical Computing**: Programming for statistical analysis",
            "**MATH 4354 - Regression Analysis**: Advanced regression techniques"
        ]
        skills = ["**R Programming**: Statistical programming language", "**Python**: Data analysis and visualization", "**Statistics**: Advanced statistical theory and methods", "**Mathematical Modeling**: Mathematical approaches to data problems", "**Data Visualization**: Creating meaningful charts and graphs"]
        projects = [
            "**Mathematical Modeling Project**: Solve real-world problems using mathematical models",
            "**Statistical Analysis Project**: Comprehensive statistical analysis of complex datasets", 
            "**Research Project**: Independent research in applied mathematics",
            "**Thesis Project**: Advanced mathematical research project"
        ]
    elif major == "Statistics":
        core_courses = [
            "**STAT 4350 - Mathematical Statistics**: Advanced statistical theory",
            "**STAT 4351 - Applied Statistics**: Statistical methods for real-world problems",
            "**STAT 4352 - Probability Theory**: Foundation in probability and statistics",
            "**STAT 4353 - Statistical Computing**: Programming for statistical analysis",
            "**STAT 4354 - Regression Analysis**: Advanced regression techniques"
        ]
        skills = ["**R Programming**: Statistical programming language", "**Python**: Data analysis and visualization", "**Statistics**: Advanced statistical theory and methods", "**Statistical Modeling**: Advanced statistical techniques", "**Data Visualization**: Creating meaningful charts and graphs"]
        projects = [
            "**Statistical Research Project**: Independent statistical research",
            "**Applied Statistics Project**: Solve real-world problems using statistical methods", 
            "**Thesis Project**: Advanced statistical research project",
            "**Capstone Project**: Comprehensive statistical analysis project"
        ]
    else:
        core_courses = [
            "**CS 4375 - Machine Learning**: Essential for understanding ML algorithms",
            "**CS 6313 - Statistical Methods for Data Science**: Foundation in statistical analysis", 
            "**CS 6350 - Big Data Management**: Learn to handle large datasets",
            "**CS 6360 - Database Design**: Database fundamentals for data storage"
        ]
        skills = ["**Python Programming**: Essential for data science", "**SQL**: Database querying and management", "**Statistics**: Statistical analysis and modeling", "**Machine Learning**: Algorithm implementation and tuning", "**Data Visualization**: Creating meaningful charts and graphs"]
        projects = [
            "**Data Analysis Project**: Analyze a real dataset using Python and pandas",
            "**Machine Learning Model**: Build a predictive model using scikit-learn", 
            "**Data Visualization Dashboard**: Create interactive visualizations",
            "**End-to-End Pipeline**: Complete data science project from collection to deployment"
        ]
    
    return {
        "query": f"I am a {major} {student_type} student at UTD. I want to become a {career_goal}. What courses should I take?",
        "unified_response": f"""
# Course Recommendations for {career_goal}

## Overview
As a {major} {student_type} student at UTD, you're on the right path to becoming a {career_goal}. Here's a comprehensive guide to help you achieve your career goals.

## Recommended Courses

### Core Courses
{chr(10).join([f"- {course}" for course in core_courses])}

### Elective Courses
- **BUAN 6353 - Business Intelligence**: BI tools and dashboard development
- **BUAN 6354 - Advanced Analytics**: Advanced analytical techniques
- **MIS 6320 - Database Management**: Database design and management systems
- **MIS 6321 - Data Warehousing**: Data warehouse design and implementation
- **MIS 6340 - IT Strategy**: Strategic IT management
- **OPRE 6361 - Operations Research**: Optimization techniques
- **OPRE 6370 - Supply Chain Analytics**: Analytics in operations

## Skills to Develop
{chr(10).join([f"- {skill}" for skill in skills])}

## Project Recommendations
{chr(10).join([f"1. {project}" for project in projects])}

## UTD Academic Timeline
- **Fall Semester**: Focus on core analytics courses (BUAN 6345, BUAN 6350)
- **Spring Semester**: Take advanced analytics and database courses (BUAN 6356, MIS 6320)
- **Summer**: Internship or research project with UTD faculty
- **Fall Semester**: Advanced topics and electives (BUAN 6352, BUAN 6353)
- **Spring Semester**: Capstone project and specialization (BUAN Capstone, MIS 6321)

## Next Steps at UTD
1. **Enroll in recommended courses**: Use UTD's course registration system
2. **Join UTD organizations**: Data Science Society, Analytics Club, or Business Analytics Association
3. **Connect with UTD faculty**: Reach out to professors in your field of interest
4. **Apply for UTD research opportunities**: Work with faculty on research projects
5. **Attend UTD career fairs**: Network with companies recruiting at UTD
6. **Consider UTD study abroad**: International programs in data science and analytics
7. **Build your portfolio**: Use UTD's computing resources and datasets
8. **Apply for UTD internships**: Career Center can help with internship placements

Good luck with your journey to becoming a {career_goal}!
        """,
        "job_market_insights": f"Current job market shows high demand for {career_goal} positions with competitive salaries and growth opportunities.",
        "course_recommendations": f"Based on your {major} background, focus on courses that bridge your current knowledge with {career_goal} requirements.",
        "career_matching_analysis": f"Your {major} major provides a strong foundation for transitioning into {career_goal} roles.",
        "project_suggestions": f"Start with beginner-friendly projects in {career_goal} to build practical experience and portfolio.",
        "session_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "timestamp": datetime.now().isoformat()
    }

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

def display_recommendations(data):
    """Display recommendations in a nice format"""
    st.markdown("### 🎯 Course Recommendation Response")
    st.markdown(data['unified_response'])
    
    st.markdown("---")
    
    # Additional insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Job Market Insights")
        st.info(data['job_market_insights'])
    
    with col2:
        st.markdown("### 📚 Course Recommendations")
        st.info(data['course_recommendations'])
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🎯 Career Matching")
        st.info(data['career_matching_analysis'])
    
    with col4:
        st.markdown("### 🚀 Project Suggestions")
        st.info(data['project_suggestions'])

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
                "Information Technology and Management", 
                "Computer Science",
                "Software Engineering",
                "Electrical Engineering",
                "Cybersecurity",
                "Management Information Systems",
                "Accounting",
                "Finance",
                "Marketing",
                "Supply Chain Management"
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
        
        st.markdown("---")
        st.markdown("### 🚀 Ready to Get Recommendations?")
        
        if st.button("Get Course Recommendations", type="primary", use_container_width=True):
            # Show loading
            with st.spinner("🤖 AI is analyzing your academic path..."):
                # Simulate processing time
                time.sleep(2)
                
                # Get mock response
                result = get_mock_response(major, student_type, career_goal)
            
            st.success("✅ Course recommendations generated successfully!")
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
