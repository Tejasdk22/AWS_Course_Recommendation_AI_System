"""
Simple Project Advisor Agent for Lambda
"""

import json
from datetime import datetime

def lambda_handler(event, context):
    """Simple project advisor handler"""
    
    try:
        query = event.get('query', '')
        session_id = event.get('sessionId', '')
        
        print(f"SimpleProjectAdvisor processing query: {query}")
        
        # Extract major from query
        major = extract_major_from_query(query)
        career_goal = extract_career_goal(query)
        
        # Generate major-specific project recommendations
        projects = generate_major_specific_projects(major, career_goal)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'SimpleProjectAdvisor',
                'query': query,
                'result': {
                    'analysis': f"Project recommendations for {major} student pursuing {career_goal}",
                    'insights': f"Generated {len(projects)} major-specific project recommendations",
                    'project_recommendations': projects,
                    'timestamp': datetime.now().isoformat()
                },
                'sessionId': session_id
            }
        }
        
    except Exception as e:
        print(f"Error in SimpleProjectAdvisor: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'SimpleProjectAdvisor'
            }
        }

def extract_major_from_query(query):
    """Extract major from query"""
    query_lower = query.lower()
    
    if 'business analytics' in query_lower or 'ba' in query_lower:
        return 'Business Analytics'
    elif 'information technology' in query_lower or 'itm' in query_lower:
        return 'Information Technology Management'
    elif 'computer science' in query_lower or 'cs' in query_lower:
        return 'Computer Science'
    else:
        return 'Business Analytics'  # Default

def extract_career_goal(query):
    """Extract career goal from query"""
    query_lower = query.lower()
    
    if 'data scientist' in query_lower:
        return 'data scientist'
    elif 'software engineer' in query_lower:
        return 'software engineer'
    elif 'business analyst' in query_lower:
        return 'business analyst'
    elif 'data analyst' in query_lower:
        return 'data analyst'
    else:
        return 'data scientist'  # Default

def generate_major_specific_projects(major, career_goal):
    """Generate major-specific project recommendations"""
    
    if major == 'Business Analytics' and career_goal == 'data scientist':
        return [
            {
                'title': 'Business Intelligence Dashboard',
                'description': 'Create an interactive BI dashboard using Tableau/Power BI to analyze business metrics and KPIs from real company data',
                'technologies': ['Tableau', 'Power BI', 'SQL', 'Excel', 'Python', 'Pandas'],
                'difficulty': 'Intermediate',
                'duration': '4-6 weeks',
                'skills_developed': ['Business Intelligence', 'Data Visualization', 'SQL', 'Business Analysis'],
                'portfolio_value': 'High',
                'major_specific': 'Perfect for BA students - combines analytics with business context'
            },
            {
                'title': 'Customer Segmentation Analysis',
                'description': 'Analyze customer data to identify market segments using clustering algorithms and create actionable business insights',
                'technologies': ['Python', 'Pandas', 'Scikit-learn', 'Matplotlib', 'Seaborn', 'Jupyter'],
                'difficulty': 'Intermediate',
                'duration': '3-4 weeks',
                'skills_developed': ['Data Analysis', 'Machine Learning', 'Python', 'Business Intelligence'],
                'portfolio_value': 'High',
                'major_specific': 'Great for BA students - practical business application'
            },
            {
                'title': 'Sales Forecasting Model',
                'description': 'Build a predictive model to forecast sales using time series analysis and machine learning techniques',
                'technologies': ['Python', 'Pandas', 'Scikit-learn', 'Prophet', 'ARIMA', 'Jupyter'],
                'difficulty': 'Advanced',
                'duration': '5-6 weeks',
                'skills_developed': ['Time Series Analysis', 'Machine Learning', 'Python', 'Business Forecasting'],
                'portfolio_value': 'Very High',
                'major_specific': 'Excellent for BA students - directly applicable to business'
            }
        ]
    
    elif major == 'Information Technology Management' and career_goal == 'software engineer':
        return [
            {
                'title': 'Enterprise Software System',
                'description': 'Build a comprehensive enterprise application with user management, reporting, and integration capabilities',
                'technologies': ['Java', 'Spring Boot', 'React', 'PostgreSQL', 'Docker', 'AWS'],
                'difficulty': 'Advanced',
                'duration': '8-10 weeks',
                'skills_developed': ['Enterprise Development', 'Java', 'System Design', 'Cloud Computing'],
                'portfolio_value': 'Very High',
                'major_specific': 'Perfect for ITM students - enterprise focus'
            },
            {
                'title': 'Cloud-Native Application',
                'description': 'Develop a scalable cloud-native application with microservices architecture and containerization',
                'technologies': ['Node.js', 'Docker', 'Kubernetes', 'AWS', 'MongoDB', 'Redis'],
                'difficulty': 'Advanced',
                'duration': '10-12 weeks',
                'skills_developed': ['Cloud Computing', 'Microservices', 'Docker', 'System Architecture'],
                'portfolio_value': 'Very High',
                'major_specific': 'Excellent for ITM students - modern cloud technologies'
            }
        ]
    
    elif major == 'Computer Science' and career_goal == 'data scientist':
        return [
            {
                'title': 'Advanced ML Model Pipeline',
                'description': 'Create a sophisticated ML pipeline with automated feature engineering, model selection, and deployment',
                'technologies': ['Python', 'Scikit-learn', 'Pandas', 'Docker', 'AWS', 'MLflow', 'Kubernetes'],
                'difficulty': 'Advanced',
                'duration': '6-8 weeks',
                'skills_developed': ['Machine Learning', 'Python', 'AWS', 'Docker', 'MLOps', 'System Design'],
                'portfolio_value': 'Very High',
                'major_specific': 'Perfect for CS students - focuses on technical depth'
            },
            {
                'title': 'Real-time Data Processing System',
                'description': 'Build a system to process streaming data using Apache Kafka, Spark, and store results in a database',
                'technologies': ['Apache Kafka', 'Apache Spark', 'Python', 'PostgreSQL', 'Docker', 'Kubernetes'],
                'difficulty': 'Advanced',
                'duration': '8-10 weeks',
                'skills_developed': ['Big Data', 'Apache Spark', 'Python', 'Database Design', 'System Architecture'],
                'portfolio_value': 'Very High',
                'major_specific': 'Excellent for CS students - complex system design'
            }
        ]
    
    else:
        # Default projects
        return [
            {
                'title': 'Portfolio Website',
                'description': 'Build a professional portfolio website showcasing your projects and skills',
                'technologies': ['HTML', 'CSS', 'JavaScript', 'React', 'GitHub Pages'],
                'difficulty': 'Beginner',
                'duration': '2-3 weeks',
                'skills_developed': ['Web Development', 'HTML', 'CSS', 'JavaScript'],
                'portfolio_value': 'Medium',
                'major_specific': 'Good starting project for any major'
            }
        ]
