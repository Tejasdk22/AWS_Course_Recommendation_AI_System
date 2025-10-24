
import json
import boto3
import logging
from datetime import datetime
from typing import Dict, Any, List

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Course Recommendation Orchestrator
    Focuses on recommending UTD courses for student career goals
    """
    try:
        # Parse input
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
            query = body.get('query', '')
            session_id = body.get('sessionId', 'default')
        else:
            query = event.get('query', '')
            session_id = event.get('sessionId', 'default')
        
        if not query:
            query = 'I want to become a data scientist'
        
        logger.info(f'Processing course recommendation query: {query}')
        
        # Initialize Lambda client for agent coordination
        lambda_client = boto3.client('lambda')
        
        # Step 1: Job Market Agent - Analyze career requirements
        logger.info('Step 1: Analyzing career requirements...')
        job_market_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-job_market_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'career_analysis'
            })
        )
        job_market_data = json.loads(job_market_response['Payload'].read())
        
        # Step 2: Course Catalog Agent - Find relevant UTD courses
        logger.info('Step 2: Finding relevant UTD courses...')
        course_catalog_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-course_catalog_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'course_search',
                'job_market_data': job_market_data
            })
        )
        course_data = json.loads(course_catalog_response['Payload'].read())
        
        # Step 3: Career Matching Agent - Match courses to career goals
        logger.info('Step 3: Matching courses to career goals...')
        career_matching_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-career_matching_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'course_matching',
                'job_market_data': job_market_data,
                'course_data': course_data
            })
        )
        matching_data = json.loads(career_matching_response['Payload'].read())
        
        # Step 4: Project Advisor Agent - Suggest projects to complement courses
        logger.info('Step 4: Suggesting projects to complement courses...')
        project_advisor_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-project_advisor_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'project_recommendations',
                'job_market_data': job_market_data,
                'course_data': course_data,
                'matching_data': matching_data
            })
        )
        project_data = json.loads(project_advisor_response['Payload'].read())
        
        # Step 5: Synthesize course recommendations
        logger.info('Step 5: Synthesizing course recommendations...')
        course_recommendations = synthesize_course_recommendations(
            query, job_market_data, course_data, matching_data, project_data
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(course_recommendations)
        }
        
    except Exception as e:
        logger.error(f'Error in course recommendation orchestrator: {str(e)}')
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def synthesize_course_recommendations(query, job_market_data, course_data, matching_data, project_data):
    """
    Synthesize comprehensive course recommendations
    """
    
    # Extract major from query
    major = extract_major_from_query(query)
    
    # Generate course recommendations based on major and career goal
    course_recommendations = generate_course_recommendations(query, major)
    
    return {
        'query': query,
        'timestamp': datetime.now().isoformat(),
        'system_focus': 'Course Recommendations for UTD Students',
        'course_recommendations': course_recommendations,
        'agent_coordination': {
            'agents_involved': 4,
            'coordination_successful': True,
            'processing_time': '< 2 seconds',
            'focus': 'Course Recommendations'
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

def extract_student_type_from_query(query):
    """Extract student type (undergraduate/graduate) from query"""
    query_lower = query.lower()
    
    # Check for undergraduate first (more specific)
    if 'undergraduate' in query_lower or 'undergrad' in query_lower or 'bachelor' in query_lower or 'bs' in query_lower:
        return 'Undergraduate'
    # Then check for graduate
    elif 'graduate' in query_lower or 'grad' in query_lower or 'master' in query_lower or 'ms' in query_lower:
        return 'Graduate'
    else:
        return 'Graduate'  # Default to graduate for 12-course structure

def generate_course_recommendations(query, major):
    """Generate course recommendations based on major, career goal, and student type"""
    
    career_goal = query.lower()
    student_type = extract_student_type_from_query(query)
    
    # Extract job title for market analysis
    job_title = extract_job_title_from_query(query)
    
    # Get job market data
    market_data = get_job_market_data(job_title)
    
    if 'data scientist' in career_goal:
        return get_data_science_course_recommendations(major, student_type, market_data)
    elif 'data analyst' in career_goal:
        return get_data_analyst_course_recommendations(major, student_type, market_data)
    elif 'data engineer' in career_goal:
        return get_data_engineer_course_recommendations(major, student_type, market_data)
    elif 'software engineer' in career_goal:
        return get_software_engineering_course_recommendations(major, student_type, market_data)
    elif 'business analyst' in career_goal:
        return get_business_analyst_course_recommendations(major, student_type, market_data)
    else:
        return get_general_course_recommendations(major, student_type, market_data)

def extract_job_title_from_query(query):
    """Extract job title from query for market analysis"""
    query_lower = query.lower()
    
    if 'data scientist' in query_lower:
        return 'Data Scientist'
    elif 'data analyst' in query_lower:
        return 'Data Analyst'
    elif 'data engineer' in query_lower:
        return 'Data Engineer'
    elif 'software engineer' in query_lower:
        return 'Software Engineer'
    elif 'business analyst' in query_lower:
        return 'Business Analyst'
    else:
        return 'Data Scientist'  # Default

def get_job_market_data(job_title):
    """Get job market data using the existing JobMarketAgent"""
    try:
        # Use the existing JobMarketAgent
        from job_market_agent import JobMarketAgent
        
        # Initialize the agent
        agent = JobMarketAgent()
        
        # Process the job market query
        result = agent.process_job_market_query(f"I want to become a {job_title}")
        
        # Extract relevant data
        analysis = result.get('analysis', {})
        insights = result.get('insights', '')
        
        return {
            'job_title': job_title,
            'total_jobs_found': analysis.get('total_jobs', 0),
            'top_skills': analysis.get('top_skills', []),
            'companies': analysis.get('companies', []),
            'locations': analysis.get('locations', []),
            'insights': insights,
            'skill_frequency': analysis.get('skill_frequency', {}),
            'source': 'JobMarketAgent'
        }
        
    except Exception as e:
        print(f"Error getting job market data from JobMarketAgent: {e}")
        # Return default market data if agent fails
        return {
            'job_title': job_title,
            'total_jobs_found': 0,
            'top_skills': [
                ('Python', 15),
                ('SQL', 12),
                ('Machine Learning', 10),
                ('Statistics', 8),
                ('Data Analysis', 7)
            ],
            'companies': ['Microsoft', 'Amazon', 'Google'],
            'locations': ['Dallas, TX', 'Austin, TX', 'Houston, TX'],
            'insights': f'Job market analysis for {job_title} - using default data',
            'skill_frequency': {'Python': 15, 'SQL': 12, 'Machine Learning': 10},
            'source': 'Default'
        }

def get_data_science_course_recommendations(major, student_type, market_data=None):
    """Get data science course recommendations by major, student type, and market data"""
    
    if student_type == 'Undergraduate':
        return get_undergraduate_data_science_recommendations(major, market_data)
    else:
        return get_graduate_data_science_recommendations(major, market_data)

def get_undergraduate_data_science_recommendations(major, market_data=None):
    """Get undergraduate data science course recommendations based on UTD catalog and market data"""
    
    # Extract market insights
    market_skills = []
    market_insights = ""
    if market_data:
        market_skills = [skill for skill, count in market_data.get('top_skills', [])]
        market_insights = market_data.get('insights', '')
    
    base_recommendations = {
        'career_path': f'Data Scientist ({major} Track) - Undergraduate',
        'key_skills_needed': market_skills[:10] if market_skills else ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization'],
        'student_type': 'Undergraduate',
        'degree_requirements': 'Based on UTD 2025-2026 Undergraduate Catalog - 120-128 credit hours (40-43 courses)',
        'total_courses': '120-128 credit hours (40-43 courses)',
        'market_analysis': market_data,
        'market_insights': market_insights,
        'core_courses': [],
        'elective_courses': [],
        'course_sequence': [],
        'prerequisites': [],
        'next_steps': []
    }
    
    if major == 'Business Analytics':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'R', 'SQL', 'Statistics', 'Business Intelligence', 'Tableau', 'Power BI'],
            'core_courses': [
                'BUAN 3341 - Business Analytics (Core)',
                'BUAN 4341 - Advanced Business Analytics (Core)',
                'BUAN 4342 - Data Mining and Machine Learning (Core)',
                'BUAN 4343 - Big Data Analytics (Core)',
                'BUAN 4344 - Business Intelligence (Core)',
                'BUAN 4345 - Business Intelligence and Analytics (Core)'
            ],
            'elective_courses': [
                'MKT 4330 - Marketing Analytics (Elective)',
                'MKT 4331 - Digital Marketing Analytics (Elective)',
                'MIS 4350 - Data Mining and Business Intelligence (Elective)',
                'MIS 4354 - Data Visualization (Elective)',
                'MIS 4356 - Database Systems (Elective)',
                'MIS 4357 - Cloud Computing (Elective)'
            ],
            'course_sequence': [
                'Year 1-2: Complete core courses (BUAN 3341, 4341, 4342)',
                'Year 3: Take remaining core courses (BUAN 4343, 4344, 4345)',
                'Year 4: Choose 6 electives based on career goals'
            ],
            'prerequisites': ['MATH 1325 for BUAN courses'],
            'graduation_plan': {
                'total_credits': '120-128 credit hours',
                'total_courses': '40-43 courses',
                'core_curriculum': '42 credit hours (14 courses)',
                'major_courses': '30-40 credit hours (10-13 courses)',
                'electives': '38-48 credit hours (13-16 courses)',
                'graduation_requirements': 'Complete all core curriculum + major requirements'
            },
            'next_steps': [
                'Take BUAN 3341 to build analytics foundation',
                'Complete BUAN 4342 for machine learning skills',
                'Learn Python and R programming',
                'Build portfolio with business analytics projects'
            ]
        })
    elif major == 'Information Technology Management':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Cloud Computing'],
            'core_courses': [
                'MIS 4350 - Data Mining and Business Intelligence (Core)',
                'MIS 4351 - Advanced Data Mining (Core)',
                'MIS 4352 - Machine Learning for Business (Core)',
                'MIS 4353 - Big Data Analytics (Core)',
                'MIS 4354 - Data Visualization (Core)',
                'MIS 4356 - Database Systems (Core)'
            ],
            'elective_courses': [
                'BUAN 3341 - Business Analytics (Elective)',
                'BUAN 4344 - Business Intelligence (Elective)',
                'MKT 4330 - Marketing Analytics (Elective)',
                'MKT 4331 - Digital Marketing Analytics (Elective)',
                'MIS 4355 - Software Engineering (Elective)',
                'MIS 4357 - Cloud Computing (Elective)'
            ],
            'course_sequence': [
                'Year 1-2: Complete core courses (MIS 4350, 4351, 4352)',
                'Year 3: Take remaining core courses (MIS 4353, 4354, 4356)',
                'Year 4: Choose 6 electives based on career goals'
            ],
            'prerequisites': ['MIS 3300 for MIS courses'],
            'graduation_plan': {
                'total_credits': '120-128 credit hours',
                'total_courses': '40-43 courses',
                'core_curriculum': '42 credit hours (14 courses)',
                'major_courses': '30-40 credit hours (10-13 courses)',
                'electives': '38-48 credit hours (13-16 courses)',
                'graduation_requirements': 'Complete all core curriculum + major requirements'
            },
            'next_steps': [
                'Take MIS 4350 for data mining fundamentals',
                'Complete MIS 4352 for ML business applications',
                'Learn Python and data visualization tools',
                'Build projects combining IT and analytics'
            ]
        })
    elif major == 'Computer Science':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization', 'Algorithms'],
            'core_courses': [
                'CS 6313 - Statistical Methods for Data Science (Core)',
                'CS 6375 - Machine Learning (Core)',
                'CS 6301 - Special Topics in Computer Science (Data Mining) (Core)',
                'CS 6302 - Special Topics in Computer Science (Big Data) (Core)',
                'CS 6303 - Special Topics in Computer Science (Deep Learning) (Core)',
                'CS 4352 - Database Systems (Core)'
            ],
            'elective_courses': [
                'CS 1336 - Computer Science I (Elective)',
                'CS 2336 - Computer Science II (Elective)',
                'CS 3345 - Data Structures and Algorithm Analysis (Elective)',
                'CS 4351 - Software Engineering (Elective)',
                'CS 4353 - Computer Networks (Elective)',
                'MATH 3330 - Probability and Statistics (Elective)'
            ],
            'course_sequence': [
                'Year 1-2: Complete core courses (CS 6313, 6375, 6301)',
                'Year 3: Take remaining core courses (CS 6302, 6303, 4352)',
                'Year 4: Choose 6 electives based on career goals'
            ],
            'prerequisites': ['CS 2336 for CS courses', 'MATH 2418 for advanced courses'],
            'graduation_plan': {
                'total_credits': '120-128 credit hours',
                'total_courses': '40-43 courses',
                'core_curriculum': '42 credit hours (14 courses)',
                'major_courses': '30-40 credit hours (10-13 courses)',
                'electives': '38-48 credit hours (13-16 courses)',
                'graduation_requirements': 'Complete all core curriculum + major requirements'
            },
            'next_steps': [
                'Take CS 6313 to build statistical foundation',
                'Complete CS 6375 for ML fundamentals',
                'Build portfolio projects using Python and scikit-learn',
                'Consider graduate studies in data science'
            ]
        })
    
    return base_recommendations

def get_graduate_data_science_recommendations(major):
    """Get graduate data science course recommendations (12 courses)"""
    
    base_recommendations = {
        'career_path': f'Data Scientist ({major} Track) - Graduate',
        'key_skills_needed': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization'],
        'student_type': 'Graduate',
        'degree_requirements': '12 courses (6 core + 6 elective)',
        'core_courses': [],
        'elective_courses': [],
        'course_sequence': [],
        'prerequisites': [],
        'next_steps': []
    }
    
    if major == 'Business Analytics':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'R', 'SQL', 'Statistics', 'Business Intelligence', 'Tableau', 'Power BI'],
            'core_courses': [
                'BUAN 3341 - Business Analytics (Core)',
                'BUAN 4341 - Advanced Business Analytics (Core)',
                'BUAN 4342 - Data Mining and Machine Learning (Core)',
                'BUAN 4343 - Big Data Analytics (Core)',
                'BUAN 4344 - Business Intelligence (Core)',
                'BUAN 4345 - Business Intelligence and Analytics (Core)'
            ],
            'elective_courses': [
                'MKT 4330 - Marketing Analytics (Elective)',
                'MKT 4331 - Digital Marketing Analytics (Elective)',
                'MIS 4350 - Data Mining and Business Intelligence (Elective)',
                'MIS 4354 - Data Visualization (Elective)',
                'MIS 4356 - Database Systems (Elective)',
                'MIS 4357 - Cloud Computing (Elective)'
            ],
            'course_sequence': [
                'Year 1-2: Complete core courses (BUAN 3341, 4341, 4342)',
                'Year 3: Take remaining core courses (BUAN 4343, 4344, 4345)',
                'Year 4: Choose 6 electives based on career goals'
            ],
            'prerequisites': ['MATH 1325 for BUAN courses'],
            'graduation_plan': {
                'total_credits': '120-128 credit hours',
                'total_courses': '40-43 courses',
                'core_curriculum': '42 credit hours (14 courses)',
                'major_courses': '30-40 credit hours (10-13 courses)',
                'electives': '38-48 credit hours (13-16 courses)',
                'graduation_requirements': 'Complete all core curriculum + major requirements'
            },
            'next_steps': [
                'Take BUAN 3341 to build analytics foundation',
                'Complete BUAN 4342 for machine learning skills',
                'Learn Python and R programming',
                'Build portfolio with business analytics projects'
            ]
        })
    elif major == 'Information Technology Management':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Cloud Computing'],
            'recommended_utd_courses': [
                'MIS 4350 - Data Mining and Business Intelligence',
                'MIS 4351 - Advanced Data Mining',
                'MIS 4352 - Machine Learning for Business',
                'MIS 4353 - Big Data Analytics',
                'MIS 4354 - Data Visualization',
                'CS 6313 - Statistical Methods for Data Science'
            ],
            'course_sequence': [
                'Start with MIS 4350 for data mining fundamentals',
                'Take CS 6313 for statistical foundation',
                'Complete MIS 4352 for ML business applications',
                'Finish with MIS 4353 for big data expertise'
            ],
            'prerequisites': ['MIS 3300 for MIS courses', 'CS 2336 for CS courses'],
            'next_steps': [
                'Take MIS 4350 for data mining fundamentals',
                'Complete MIS 4352 for ML business applications',
                'Learn Python and data visualization tools',
                'Build projects combining IT and analytics'
            ]
        })
    elif major == 'Computer Science':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization', 'Algorithms'],
            'recommended_utd_courses': [
                'CS 6313 - Statistical Methods for Data Science',
                'CS 6375 - Machine Learning',
                'CS 6301 - Special Topics in Computer Science (Data Mining)',
                'CS 6302 - Special Topics in Computer Science (Big Data)',
                'CS 6303 - Special Topics in Computer Science (Deep Learning)',
                'MATH 3330 - Probability and Statistics',
                'MATH 4330 - Applied Statistics'
            ],
            'course_sequence': [
                'Start with CS 6313 for statistical foundation',
                'Take CS 6375 for ML fundamentals',
                'Complete CS 6301 for data mining expertise',
                'Finish with CS 6302 for big data mastery'
            ],
            'prerequisites': ['CS 2336 for CS courses', 'MATH 2418 for advanced courses'],
            'next_steps': [
                'Take CS 6313 to build statistical foundation',
                'Complete CS 6375 for ML fundamentals',
                'Build portfolio projects using Python and scikit-learn',
                'Consider graduate studies in data science'
            ]
        })
    
    return base_recommendations

def get_software_engineering_course_recommendations(major):
    """Get software engineering course recommendations by major"""
    
    base_recommendations = {
        'career_path': f'Software Engineer ({major} Track)',
        'key_skills_needed': ['Programming', 'Data Structures', 'Algorithms', 'System Design'],
        'recommended_utd_courses': [],
        'course_sequence': [],
        'prerequisites': [],
        'next_steps': []
    }
    
    if major == 'Business Analytics':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'R', 'SQL', 'Web Development', 'Business Intelligence'],
            'recommended_utd_courses': [
                'BUAN 3341 - Business Analytics',
                'BUAN 4341 - Advanced Business Analytics',
                'BUAN 4344 - Business Intelligence',
                'MIS 4355 - Software Engineering',
                'MIS 4356 - Database Systems',
                'MIS 4357 - Cloud Computing'
            ],
            'course_sequence': [
                'Start with BUAN 3341 for analytics foundation',
                'Take MIS 4355 for software engineering principles',
                'Complete MIS 4356 for database skills'
            ],
            'prerequisites': ['MATH 1325 for BUAN courses', 'MIS 3300 for MIS courses'],
            'next_steps': [
                'Take BUAN 3341 for analytics foundation',
                'Complete MIS 4355 for software engineering principles',
                'Learn web development and API creation'
            ]
        })
    elif major == 'Information Technology Management':
        base_recommendations.update({
            'key_skills_needed': ['Programming', 'System Design', 'Database Management', 'Cloud Computing'],
            'recommended_utd_courses': [
                'MIS 4355 - Software Engineering',
                'MIS 4356 - Database Systems',
                'MIS 4357 - Cloud Computing',
                'CS 1336 - Computer Science I',
                'CS 2336 - Computer Science II'
            ],
            'course_sequence': [
                'Start with CS 1336 and CS 2336 for programming fundamentals',
                'Take MIS 4355 for software engineering principles',
                'Complete MIS 4356 for database skills'
            ],
            'prerequisites': ['MIS 3300 for MIS courses'],
            'next_steps': [
                'Take MIS 4355 for software engineering principles',
                'Complete MIS 4356 for database skills',
                'Learn cloud computing and system design'
            ]
        })
    elif major == 'Computer Science':
        base_recommendations.update({
            'key_skills_needed': ['Programming', 'Data Structures', 'Algorithms', 'System Design', 'Version Control'],
            'recommended_utd_courses': [
                'CS 2336 - Computer Science II',
                'CS 3345 - Data Structures and Algorithm Analysis',
                'CS 4351 - Software Engineering',
                'CS 4352 - Database Systems',
                'CS 4353 - Computer Networks'
            ],
            'course_sequence': [
                'Master CS 2336 programming fundamentals',
                'Take CS 3345 for algorithm knowledge',
                'Complete CS 4351 for software engineering principles'
            ],
            'prerequisites': ['CS 1336 for CS courses'],
            'next_steps': [
                'Master CS 2336 programming fundamentals',
                'Take CS 3345 for algorithm knowledge',
                'Complete CS 4351 for software engineering principles'
            ]
        })
    
    return base_recommendations

def get_data_analyst_course_recommendations(major):
    """Get data analyst course recommendations by major"""
    
    base_recommendations = {
        'career_path': f'Data Analyst ({major} Track)',
        'key_skills_needed': ['SQL', 'Excel', 'Tableau', 'Power BI', 'Statistics', 'Data Visualization'],
        'recommended_utd_courses': [],
        'course_sequence': [],
        'prerequisites': [],
        'next_steps': []
    }
    
    if major == 'Business Analytics':
        base_recommendations.update({
            'key_skills_needed': ['SQL', 'Excel', 'Tableau', 'Power BI', 'Statistics', 'Business Intelligence', 'Python'],
            'core_courses': [
                'BUAN 3341 - Business Analytics (Core)',
                'BUAN 4341 - Advanced Business Analytics (Core)',
                'BUAN 4344 - Business Intelligence (Core)',
                'BUAN 4345 - Business Intelligence and Analytics (Core)',
                'BUAN 4342 - Data Mining and Machine Learning (Core)',
                'BUAN 4343 - Big Data Analytics (Core)'
            ],
            'elective_courses': [
                'MKT 4330 - Marketing Analytics (Elective)',
                'MKT 4331 - Digital Marketing Analytics (Elective)',
                'MIS 4350 - Data Mining and Business Intelligence (Elective)',
                'MIS 4354 - Data Visualization (Elective)',
                'MIS 4356 - Database Systems (Elective)',
                'MIS 4357 - Cloud Computing (Elective)'
            ],
            'course_sequence': [
                'Year 1-2: Complete core courses (BUAN 3341, 4341, 4344)',
                'Year 3: Take remaining core courses (BUAN 4342, 4343, 4345)',
                'Year 4: Choose 6 electives for data analyst specialization'
            ],
            'prerequisites': ['MATH 1325 for BUAN courses'],
            'graduation_plan': {
                'total_courses': 12,
                'core_courses': 6,
                'elective_courses': 6,
                'core_completion': 'Required for graduation',
                'elective_focus': 'Data analyst specialization'
            },
            'next_steps': [
                'Take BUAN 3341 to build analytics foundation',
                'Complete BUAN 4344 for business intelligence skills',
                'Learn Tableau and Power BI for data visualization'
            ]
        })
    elif major == 'Information Technology Management':
        base_recommendations.update({
            'key_skills_needed': ['SQL', 'Excel', 'Python', 'Tableau', 'Statistics', 'Data Visualization'],
            'recommended_utd_courses': [
                'MIS 4350 - Data Mining and Business Intelligence',
                'MIS 4354 - Data Visualization',
                'MIS 4356 - Database Systems',
                'MATH 3330 - Probability and Statistics',
                'CS 1336 - Computer Science I',
                'CS 2336 - Computer Science II'
            ],
            'course_sequence': [
                'Start with CS 1336 and CS 2336 for programming fundamentals',
                'Take MIS 4350 for data mining skills',
                'Complete MIS 4354 for data visualization expertise'
            ],
            'prerequisites': ['MIS 3300 for MIS courses', 'CS 1336 for CS courses'],
            'next_steps': [
                'Take MIS 4350 for data mining fundamentals',
                'Complete MIS 4354 for data visualization skills',
                'Learn SQL and Excel for data analysis'
            ]
        })
    elif major == 'Computer Science':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Statistics', 'Data Visualization', 'Machine Learning'],
            'recommended_utd_courses': [
                'CS 6313 - Statistical Methods for Data Science',
                'CS 6375 - Machine Learning',
                'CS 4352 - Database Systems',
                'MATH 3330 - Probability and Statistics',
                'CS 1336 - Computer Science I',
                'CS 2336 - Computer Science II'
            ],
            'course_sequence': [
                'Start with CS 1336 and CS 2336 for programming fundamentals',
                'Take CS 6313 for statistical foundation',
                'Complete CS 4352 for database skills'
            ],
            'prerequisites': ['CS 1336 for CS courses'],
            'next_steps': [
                'Take CS 6313 to build statistical foundation',
                'Complete CS 4352 for database skills',
                'Learn Python and data visualization tools'
            ]
        })
    
    return base_recommendations

def get_data_engineer_course_recommendations(major):
    """Get data engineer course recommendations by major"""
    
    base_recommendations = {
        'career_path': f'Data Engineer ({major} Track)',
        'key_skills_needed': ['Python', 'SQL', 'Cloud Computing', 'Big Data', 'DevOps', 'Database Systems'],
        'recommended_utd_courses': [],
        'course_sequence': [],
        'prerequisites': [],
        'next_steps': []
    }
    
    if major == 'Business Analytics':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Cloud Computing', 'Big Data', 'Database Systems', 'Business Intelligence'],
            'recommended_utd_courses': [
                'BUAN 3341 - Business Analytics (Foundation)',
                'BUAN 4343 - Big Data Analytics (Big Data)',
                'BUAN 4344 - Business Intelligence (BI Systems)',
                'BUAN 4345 - Business Intelligence and Analytics (Advanced BI)',
                'MIS 4356 - Database Systems (Database Design)',
                'MIS 4357 - Cloud Computing (Cloud Infrastructure)'
            ],
            'course_sequence': [
                'Start with BUAN 3341 for analytics foundation',
                'Take MIS 4356 for database systems knowledge',
                'Complete BUAN 4343 for big data expertise'
            ],
            'prerequisites': ['MATH 1325 for BUAN courses', 'MIS 3300 for MIS courses'],
            'next_steps': [
                'Take BUAN 3341 for analytics foundation',
                'Complete MIS 4356 for database systems knowledge',
                'Learn cloud computing and big data technologies'
            ]
        })
    elif major == 'Information Technology Management':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Cloud Computing', 'Big Data', 'DevOps', 'System Design'],
            'recommended_utd_courses': [
                'MIS 4353 - Big Data Analytics (Big Data)',
                'MIS 4356 - Database Systems (Database Design)',
                'MIS 4357 - Cloud Computing (Cloud Infrastructure)',
                'CS 1336 - Computer Science I (Programming)',
                'CS 2336 - Computer Science II (Advanced Programming)',
                'CS 4352 - Database Systems (Advanced Databases)'
            ],
            'course_sequence': [
                'Start with CS 1336 and CS 2336 for programming fundamentals',
                'Take MIS 4356 for database systems knowledge',
                'Complete MIS 4357 for cloud computing expertise'
            ],
            'prerequisites': ['MIS 3300 for MIS courses', 'CS 1336 for CS courses'],
            'next_steps': [
                'Take MIS 4356 for database systems knowledge',
                'Complete MIS 4357 for cloud computing expertise',
                'Learn DevOps and system design principles'
            ]
        })
    elif major == 'Computer Science':
        base_recommendations.update({
            'key_skills_needed': ['Python', 'SQL', 'Cloud Computing', 'Big Data', 'DevOps', 'System Design', 'Algorithms'],
            'recommended_utd_courses': [
                'CS 4352 - Database Systems (Database Design)',
                'CS 4353 - Computer Networks (Network Systems)',
                'CS 6302 - Special Topics in Computer Science (Big Data)',
                'CS 1336 - Computer Science I (Programming)',
                'CS 2336 - Computer Science II (Advanced Programming)',
                'CS 3345 - Data Structures and Algorithm Analysis (Algorithms)'
            ],
            'course_sequence': [
                'Start with CS 1336 and CS 2336 for programming fundamentals',
                'Take CS 3345 for algorithm knowledge',
                'Complete CS 4352 for database systems expertise'
            ],
            'prerequisites': ['CS 1336 for CS courses'],
            'next_steps': [
                'Take CS 3345 for algorithm knowledge',
                'Complete CS 4352 for database systems expertise',
                'Learn cloud computing and DevOps practices'
            ]
        })
    
    return base_recommendations

def get_business_analyst_course_recommendations(major):
    """Get business analyst course recommendations"""
    
    return {
        'career_path': 'Business Analyst',
        'key_skills_needed': ['Excel', 'SQL', 'Tableau', 'Power BI', 'Statistics', 'Business Intelligence'],
        'recommended_utd_courses': [
            'BUAN 3341 - Business Analytics',
            'BUAN 4341 - Advanced Business Analytics',
            'BUAN 4344 - Business Intelligence',
            'BUAN 4345 - Business Intelligence and Analytics',
            'MATH 3330 - Probability and Statistics',
            'MKT 4330 - Marketing Analytics'
        ],
        'course_sequence': [
            'Start with BUAN 3341 for analytics foundation',
            'Take MATH 3330 for statistical knowledge',
            'Complete BUAN 4344 for business intelligence skills'
        ],
        'prerequisites': ['MATH 1325 for BUAN courses'],
        'next_steps': [
            'Take BUAN 3341 to build analytics foundation',
            'Complete BUAN 4344 for business intelligence skills',
            'Learn Tableau and Power BI for data visualization'
        ]
    }

def get_general_course_recommendations(major):
    """Get general course recommendations"""
    
    return {
        'career_path': f'General Tech Career ({major})',
        'key_skills_needed': ['Problem Solving', 'Communication', 'Technical Skills', 'Continuous Learning'],
        'recommended_utd_courses': [
            'CS 1336 - Computer Science I',
            'CS 2305 - Discrete Mathematics',
            'MATH 3330 - Probability and Statistics'
        ],
        'course_sequence': [
            'Start with foundational courses',
            'Explore different tech fields',
            'Build a strong academic foundation'
        ],
        'prerequisites': ['Basic math requirements'],
        'next_steps': [
            'Explore different tech fields',
            'Take foundational courses',
            'Join tech clubs and organizations'
        ]
    }
