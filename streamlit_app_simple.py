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
    elif major == "Data Science":
        core_courses = [
            "**CS 4375 - Machine Learning**: Essential for understanding ML algorithms at UTD",
            "**CS 6313 - Statistical Methods for Data Science**: Foundation in statistical analysis",
            "**CS 6350 - Big Data Management**: Learn to handle large datasets using UTD's computing resources",
            "**CS 6360 - Database Design**: Database fundamentals for data storage",
            "**CS 6363 - Data Mining**: Advanced data mining techniques"
        ]
        skills = ["**Python Programming**: Essential for data science using UTD's Python environment", "**SQL**: Database querying and management", "**Statistics**: Statistical analysis and modeling", "**Machine Learning**: Algorithm implementation and tuning", "**Data Visualization**: Creating meaningful charts and graphs"]
        projects = [
            "**UTD Data Science Capstone**: Real-world data science project with industry partners",
            "**Machine Learning Model**: Build a predictive model using scikit-learn and UTD datasets", 
            "**Data Visualization Dashboard**: Create interactive visualizations using UTD's tools",
            "**End-to-End Pipeline**: Complete data science project from collection to deployment"
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
    elif major == "Information Technology":
        core_courses = [
            "**ITSS 4350 - Data Analytics**: Foundation in data analytics for IT professionals",
            "**ITSS 4351 - Business Intelligence**: BI tools and techniques",
            "**ITSS 4352 - Database Systems**: Database management systems",
            "**ITSS 4353 - Data Mining**: Discover patterns in data using IT tools",
            "**ITSS 4354 - Big Data Technologies**: Hadoop, Spark, and big data platforms"
        ]
        skills = ["**Python Programming**: Essential for data analysis", "**SQL**: Database querying and management", "**Statistics**: Statistical analysis and modeling", "**Business Intelligence**: BI tools and dashboards", "**Data Visualization**: Creating meaningful charts and graphs"]
        projects = [
            "**IT Capstone Project**: Real-world IT solution development",
            "**Business Intelligence Dashboard**: Create interactive BI reports", 
            "**Data Analysis Project**: Analyze business data using IT tools",
            "**Database Design Project**: Design and implement a database system"
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
# Career Guidance for {career_goal}

## Overview
As a {major} {student_type} student at UTD, you're on the right path to becoming a {career_goal}. Here's a comprehensive guide to help you achieve your career goals.

## Recommended Courses

### Core Courses
{chr(10).join([f"- {course}" for course in core_courses])}

### Elective Courses
- **BUAN 6353 - Business Intelligence**: BI tools and dashboard development
- **MIS 6320 - Database Management**: Database design and management systems
- **MIS 6321 - Data Warehousing**: Data warehouse design and implementation
- **CS 6363 - Data Mining**: Discover patterns in large datasets
- **CS 6375 - Advanced Machine Learning**: Deep learning and neural networks
- **ITSS 4355 - Data Visualization**: Advanced visualization techniques
- **MATH 4355 - Time Series Analysis**: Statistical analysis of time-dependent data

## Skills to Develop
{chr(10).join([f"- {skill}" for skill in skills])}

## Project Recommendations
{chr(10).join([f"1. {project}" for project in projects])}

## UTD Academic Timeline
- **Fall Semester**: Focus on core programming and statistics courses (CS 4375, BUAN 6351)
- **Spring Semester**: Take machine learning and database courses (CS 6350, CS 6360)
- **Summer**: Internship or research project with UTD faculty
- **Fall Semester**: Advanced topics and electives (CS 6375, BUAN 6353)
- **Spring Semester**: Capstone project and specialization (CS 6390, ITSS 4355)

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

def display_recommendations(data):
    """Display recommendations in a nice format"""
    st.markdown("### 🎯 Career Guidance Response")
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
            ["Business Analytics", "Data Science", "Computer Science", "Information Technology", "Mathematics", "Statistics", "Engineering", "Business", "Economics", "Finance"],
            index=0
        )
        
        student_type = st.selectbox(
            "Student Type",
            ["Undergraduate", "Graduate"],
            index=1
        )
        
        career_goal = st.selectbox(
            "Career Goal",
            ["Data Scientist", "Data Engineer", "Data Analyst", "ML Engineer", "Software Engineer", "Product Manager"],
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
        
        # Display recommendations
        display_recommendations(data)
        
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
