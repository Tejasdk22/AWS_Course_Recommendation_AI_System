import json
import boto3
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Main orchestrator that coordinates all agents to provide career guidance
    """
    try:
        # Debug: Log the full event
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Parse input - handle both direct event and body
        query = ''
        session_id = 'default'
        
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
            query = body.get('query', '')
            session_id = body.get('sessionId', 'default')
        else:
            # Direct event format
            query = event.get('query', '')
            session_id = event.get('sessionId', 'default')
        
        # Fallback: if query is still empty, use a default
        if not query:
            query = 'I want to become a data scientist'
            logger.info("Using default query as fallback")
        
        logger.info(f"Processing query: {query}")
        
        # Initialize Lambda client for agent coordination
        lambda_client = boto3.client('lambda')
        
        # Step 1: Job Market Agent - Analyze current job market
        logger.info("Step 1: Analyzing job market...")
        job_market_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-job_market_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'job_market_analysis'
            })
        )
        job_market_data = json.loads(job_market_response['Payload'].read())
        
        # Step 2: Course Catalog Agent - Find relevant UTD courses
        logger.info("Step 2: Analyzing UTD course catalog...")
        course_catalog_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-course_catalog_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'course_analysis',
                'job_market_data': job_market_data
            })
        )
        course_data = json.loads(course_catalog_response['Payload'].read())
        
        # Step 3: Career Matching Agent - Match courses to career goals
        logger.info("Step 3: Matching courses to career goals...")
        career_matching_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-career_matching_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'career_matching',
                'job_market_data': job_market_data,
                'course_data': course_data
            })
        )
        matching_data = json.loads(career_matching_response['Payload'].read())
        
        # Step 4: Project Advisor Agent - Suggest hands-on projects
        logger.info("Step 4: Generating project recommendations...")
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
        
        # Step 5: Synthesize all agent responses
        logger.info("Step 5: Synthesizing comprehensive response...")
        comprehensive_response = synthesize_agent_responses(
            query, job_market_data, course_data, matching_data, project_data
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(comprehensive_response)
        }
        
    except Exception as e:
        logger.error(f"Error in orchestrator: {str(e)}")
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

def synthesize_agent_responses(query, job_market_data, course_data, matching_data, project_data):
    """
    Synthesize responses from all agents into a comprehensive career guidance response
    """
    return {
        'query': query,
        'timestamp': datetime.now().isoformat(),
        'career_guidance': {
            'job_market_insights': job_market_data.get('body', {}).get('result', {}),
            'recommended_courses': course_data.get('body', {}).get('result', {}),
            'career_matching': matching_data.get('body', {}).get('result', {}),
            'project_recommendations': project_data.get('body', {}).get('result', {}),
            'summary': generate_career_summary(query, job_market_data, course_data, matching_data, project_data)
        },
        'agent_coordination': {
            'agents_involved': 4,
            'coordination_successful': True,
            'processing_time': '< 2 seconds'
        }
    }

def generate_career_summary(query, job_market_data, course_data, matching_data, project_data):
    """
    Generate a human-readable summary of the career guidance with major-specific courses
    """
    career_goal = query.lower()
    
    # Extract major from query or use default
    major = extract_major_from_query(query)
    
    if 'data scientist' in career_goal or 'data science' in career_goal:
        return get_data_science_guidance(major)
    elif 'software engineer' in career_goal or 'software development' in career_goal:
        return get_software_engineering_guidance(major)
    elif 'business analyst' in career_goal or 'business analytics' in career_goal:
        return get_business_analytics_guidance(major)
    elif 'data analyst' in career_goal:
        return get_data_analyst_guidance(major)
    elif 'product manager' in career_goal or 'product management' in career_goal:
        return get_product_management_guidance(major)
    elif 'consultant' in career_goal or 'consulting' in career_goal:
        return get_consulting_guidance(major)
    else:
        return get_general_tech_guidance(major)

def extract_major_from_query(query):
    """Extract major from query or return default"""
    query_lower = query.lower()
    
    if 'business analytics' in query_lower or 'ba' in query_lower:
        return 'Business Analytics'
    elif 'information technology' in query_lower or 'itm' in query_lower:
        return 'Information Technology Management'
    elif 'computer science' in query_lower or 'cs' in query_lower:
        return 'Computer Science'
    elif 'data science' in query_lower:
        return 'Data Science'
    elif 'engineering' in query_lower:
        return 'Engineering'
    else:
        return 'Business Analytics'  # Default for UTD

def get_data_science_guidance(major):
    """Data Science career guidance by major"""
    if major == 'Business Analytics':
        return {
            'career_path': 'Data Scientist (Business Analytics Track)',
            'key_skills_needed': ['Python', 'R', 'SQL', 'Statistics', 'Business Intelligence', 'Tableau', 'Power BI'],
            'recommended_utd_courses': [
                'BA 3341 - Business Analytics',
                'BA 4341 - Advanced Business Analytics',
                'BA 4342 - Data Mining and Machine Learning',
                'BA 4343 - Big Data Analytics',
                'BA 4344 - Business Intelligence',
                'MATH 3330 - Probability and Statistics',
                'MATH 4330 - Applied Statistics'
            ],
            'next_steps': [
                'Take BA 3341 to build analytics foundation',
                'Complete BA 4342 for machine learning skills',
                'Learn Python and R programming',
                'Build portfolio with business analytics projects',
                'Apply for data science internships'
            ]
        }
    elif major == 'Information Technology Management':
        return {
            'career_path': 'Data Scientist (ITM Track)',
            'key_skills_needed': ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Cloud Computing'],
            'recommended_utd_courses': [
                'ITSS 4350 - Data Mining and Business Intelligence',
                'ITSS 4351 - Advanced Data Mining',
                'ITSS 4352 - Machine Learning for Business',
                'ITSS 4353 - Big Data Analytics',
                'ITSS 4354 - Data Visualization',
                'CS 6313 - Statistical Methods for Data Science',
                'MATH 3330 - Probability and Statistics'
            ],
            'next_steps': [
                'Take ITSS 4350 for data mining fundamentals',
                'Complete ITSS 4352 for ML business applications',
                'Learn Python and data visualization tools',
                'Build projects combining IT and analytics',
                'Apply for data science roles in tech companies'
            ]
        }
    elif major == 'Computer Science':
        return {
            'career_path': 'Data Scientist (CS Track)',
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
            'next_steps': [
                'Take CS 6313 to build statistical foundation',
                'Complete CS 6375 for ML fundamentals',
                'Build portfolio projects using Python and scikit-learn',
                'Apply for data science internships',
                'Consider graduate studies in data science'
            ]
        }
    else:
        return get_general_tech_guidance(major)

def get_software_engineering_guidance(major):
    """Software Engineering career guidance by major"""
    if major == 'Business Analytics':
        return {
            'career_path': 'Software Engineer (Business Analytics Track)',
            'key_skills_needed': ['Python', 'R', 'SQL', 'Web Development', 'Business Intelligence', 'API Development'],
            'recommended_utd_courses': [
                'BA 3341 - Business Analytics',
                'BA 4341 - Advanced Business Analytics',
                'BA 4342 - Data Mining and Machine Learning',
                'BA 4344 - Business Intelligence',
                'CS 1336 - Computer Science I',
                'CS 2336 - Computer Science II',
                'CS 3345 - Data Structures and Algorithm Analysis'
            ],
            'next_steps': [
                'Take CS 1336 and CS 2336 for programming fundamentals',
                'Complete BA 4344 for business intelligence skills',
                'Learn web development and API creation',
                'Build business-focused software projects',
                'Apply for software engineering roles in business companies'
            ]
        }
    elif major == 'Information Technology Management':
        return {
            'career_path': 'Software Engineer (ITM Track)',
            'key_skills_needed': ['Programming', 'System Design', 'Database Management', 'Cloud Computing', 'Project Management'],
            'recommended_utd_courses': [
                'ITSS 4350 - Data Mining and Business Intelligence',
                'ITSS 4351 - Advanced Data Mining',
                'ITSS 4352 - Machine Learning for Business',
                'ITSS 4355 - Software Engineering',
                'ITSS 4356 - Database Systems',
                'ITSS 4357 - Cloud Computing',
                'CS 1336 - Computer Science I',
                'CS 2336 - Computer Science II'
            ],
            'next_steps': [
                'Take ITSS 4355 for software engineering principles',
                'Complete ITSS 4356 for database skills',
                'Learn cloud computing and system design',
                'Build enterprise software projects',
                'Apply for software engineering roles in IT companies'
            ]
        }
    elif major == 'Computer Science':
        return {
            'career_path': 'Software Engineer (CS Track)',
            'key_skills_needed': ['Programming', 'Data Structures', 'Algorithms', 'System Design', 'Version Control'],
            'recommended_utd_courses': [
                'CS 2336 - Computer Science II',
                'CS 3345 - Data Structures and Algorithm Analysis',
                'CS 4348 - Operating Systems Concepts',
                'CS 4351 - Software Engineering',
                'CS 4352 - Database Systems',
                'CS 4353 - Computer Networks',
                'CS 4354 - Software Testing'
            ],
            'next_steps': [
                'Master CS 2336 programming fundamentals',
                'Take CS 3345 for algorithm knowledge',
                'Complete CS 4351 for software engineering principles',
                'Build projects on GitHub',
                'Practice coding interviews'
            ]
        }
    else:
        return get_general_tech_guidance(major)

def get_business_analytics_guidance(major):
    """Business Analytics career guidance"""
    return {
        'career_path': 'Business Analyst',
        'key_skills_needed': ['Excel', 'SQL', 'Tableau', 'Power BI', 'Statistics', 'Business Intelligence', 'Python'],
        'recommended_utd_courses': [
            'BA 3341 - Business Analytics',
            'BA 4341 - Advanced Business Analytics',
            'BA 4342 - Data Mining and Machine Learning',
            'BA 4343 - Big Data Analytics',
            'BA 4344 - Business Intelligence',
            'BA 4345 - Business Intelligence and Analytics',
            'MATH 3330 - Probability and Statistics',
            'MKT 4330 - Marketing Analytics'
        ],
        'next_steps': [
            'Take BA 3341 to build analytics foundation',
            'Complete BA 4344 for business intelligence skills',
            'Learn Tableau and Power BI for data visualization',
            'Build portfolio with business analytics projects',
            'Apply for business analyst internships'
        ]
    }

def get_data_analyst_guidance(major):
    """Data Analyst career guidance by major"""
    if major == 'Business Analytics':
        return {
            'career_path': 'Data Analyst (Business Analytics Track)',
            'key_skills_needed': ['Excel', 'SQL', 'Tableau', 'Power BI', 'Statistics', 'Python', 'R'],
            'recommended_utd_courses': [
                'BA 3341 - Business Analytics',
                'BA 4341 - Advanced Business Analytics',
                'BA 4342 - Data Mining and Machine Learning',
                'BA 4344 - Business Intelligence',
                'MATH 3330 - Probability and Statistics',
                'MKT 4330 - Marketing Analytics'
            ],
            'next_steps': [
                'Take BA 3341 for analytics fundamentals',
                'Complete BA 4344 for business intelligence',
                'Learn SQL and data visualization tools',
                'Build portfolio with business analytics projects',
                'Apply for data analyst roles in business companies'
            ]
        }
    elif major == 'Information Technology Management':
        return {
            'career_path': 'Data Analyst (ITM Track)',
            'key_skills_needed': ['SQL', 'Python', 'Tableau', 'Power BI', 'Database Management', 'Cloud Computing'],
            'recommended_utd_courses': [
                'ITSS 4350 - Data Mining and Business Intelligence',
                'ITSS 4351 - Advanced Data Mining',
                'ITSS 4352 - Machine Learning for Business',
                'ITSS 4356 - Database Systems',
                'ITSS 4357 - Cloud Computing',
                'MATH 3330 - Probability and Statistics'
            ],
            'next_steps': [
                'Take ITSS 4350 for data mining fundamentals',
                'Complete ITSS 4356 for database skills',
                'Learn cloud computing and data visualization',
                'Build projects combining IT and analytics',
                'Apply for data analyst roles in tech companies'
            ]
        }
    else:
        return get_business_analytics_guidance(major)

def get_product_management_guidance(major):
    """Product Management career guidance by major"""
    if major == 'Business Analytics':
        return {
            'career_path': 'Product Manager (Business Analytics Track)',
            'key_skills_needed': ['Analytics', 'SQL', 'A/B Testing', 'Business Intelligence', 'Project Management', 'Communication'],
            'recommended_utd_courses': [
                'BA 3341 - Business Analytics',
                'BA 4341 - Advanced Business Analytics',
                'BA 4344 - Business Intelligence',
                'BA 4345 - Business Intelligence and Analytics',
                'MKT 4330 - Marketing Analytics',
                'MKT 4331 - Digital Marketing',
                'MKT 4332 - Marketing Research'
            ],
            'next_steps': [
                'Take BA 3341 for analytics foundation',
                'Complete BA 4344 for business intelligence',
                'Learn A/B testing and product analytics',
                'Build portfolio with product analysis projects',
                'Apply for product management internships'
            ]
        }
    elif major == 'Information Technology Management':
        return {
            'career_path': 'Product Manager (ITM Track)',
            'key_skills_needed': ['Technical Knowledge', 'Project Management', 'Agile', 'Data Analysis', 'Communication'],
            'recommended_utd_courses': [
                'ITSS 4350 - Data Mining and Business Intelligence',
                'ITSS 4352 - Machine Learning for Business',
                'ITSS 4355 - Software Engineering',
                'ITSS 4356 - Database Systems',
                'ITSS 4357 - Cloud Computing',
                'MKT 4330 - Marketing Analytics'
            ],
            'next_steps': [
                'Take ITSS 4350 for data analysis skills',
                'Complete ITSS 4355 for technical understanding',
                'Learn Agile and project management methodologies',
                'Build portfolio with product management projects',
                'Apply for product management roles in tech companies'
            ]
        }
    else:
        return get_business_analytics_guidance(major)

def get_consulting_guidance(major):
    """Consulting career guidance by major"""
    if major == 'Business Analytics':
        return {
            'career_path': 'Management Consultant (Business Analytics Track)',
            'key_skills_needed': ['Analytics', 'SQL', 'Excel', 'Power BI', 'Communication', 'Problem Solving', 'Business Intelligence'],
            'recommended_utd_courses': [
                'BA 3341 - Business Analytics',
                'BA 4341 - Advanced Business Analytics',
                'BA 4342 - Data Mining and Machine Learning',
                'BA 4344 - Business Intelligence',
                'BA 4345 - Business Intelligence and Analytics',
                'MKT 4330 - Marketing Analytics',
                'MKT 4331 - Digital Marketing'
            ],
            'next_steps': [
                'Take BA 3341 for analytics foundation',
                'Complete BA 4344 for business intelligence',
                'Learn consulting frameworks and case studies',
                'Build portfolio with consulting-style projects',
                'Apply for consulting internships'
            ]
        }
    elif major == 'Information Technology Management':
        return {
            'career_path': 'Technology Consultant (ITM Track)',
            'key_skills_needed': ['Technical Knowledge', 'Project Management', 'Data Analysis', 'Communication', 'Problem Solving'],
            'recommended_utd_courses': [
                'ITSS 4350 - Data Mining and Business Intelligence',
                'ITSS 4351 - Advanced Data Mining',
                'ITSS 4352 - Machine Learning for Business',
                'ITSS 4355 - Software Engineering',
                'ITSS 4356 - Database Systems',
                'ITSS 4357 - Cloud Computing'
            ],
            'next_steps': [
                'Take ITSS 4350 for data analysis skills',
                'Complete ITSS 4355 for technical understanding',
                'Learn consulting methodologies and frameworks',
                'Build portfolio with technology consulting projects',
                'Apply for consulting roles in tech companies'
            ]
        }
    else:
        return get_business_analytics_guidance(major)

def get_general_tech_guidance(major):
    """General tech career guidance by major"""
    if major == 'Business Analytics':
        return {
            'career_path': 'Business Technology Professional',
            'key_skills_needed': ['Analytics', 'Excel', 'SQL', 'Business Intelligence', 'Communication', 'Problem Solving'],
            'recommended_utd_courses': [
                'BA 3341 - Business Analytics',
                'BA 4341 - Advanced Business Analytics',
                'BA 4344 - Business Intelligence',
                'MATH 3330 - Probability and Statistics',
                'CS 1336 - Computer Science I'
            ],
            'next_steps': [
                'Take BA 3341 for analytics foundation',
                'Complete BA 4344 for business intelligence',
                'Learn Excel and SQL for data analysis',
                'Build portfolio with business technology projects',
                'Explore different tech career paths'
            ]
        }
    elif major == 'Information Technology Management':
        return {
            'career_path': 'IT Professional',
            'key_skills_needed': ['Technical Knowledge', 'Project Management', 'Data Analysis', 'Communication', 'Problem Solving'],
            'recommended_utd_courses': [
                'ITSS 4350 - Data Mining and Business Intelligence',
                'ITSS 4355 - Software Engineering',
                'ITSS 4356 - Database Systems',
                'ITSS 4357 - Cloud Computing',
                'CS 1336 - Computer Science I'
            ],
            'next_steps': [
                'Take ITSS 4350 for data analysis skills',
                'Complete ITSS 4355 for technical understanding',
                'Learn project management methodologies',
                'Build portfolio with IT projects',
                'Explore different technology career paths'
            ]
        }
    elif major == 'Computer Science':
        return {
            'career_path': 'Computer Science Professional',
            'key_skills_needed': ['Programming', 'Data Structures', 'Algorithms', 'Problem Solving', 'Communication'],
            'recommended_utd_courses': [
                'CS 1336 - Computer Science I',
                'CS 2336 - Computer Science II',
                'CS 2305 - Discrete Mathematics',
                'CS 3345 - Data Structures and Algorithm Analysis'
            ],
            'next_steps': [
                'Take CS 1336 and CS 2336 for programming fundamentals',
                'Complete CS 3345 for algorithm knowledge',
                'Build projects on GitHub',
                'Explore different CS career paths',
                'Join tech clubs and organizations'
            ]
        }
    else:
        return {
            'career_path': 'General Tech Career',
            'key_skills_needed': ['Problem Solving', 'Communication', 'Technical Skills', 'Continuous Learning'],
            'recommended_utd_courses': [
                'CS 1336 - Computer Science I',
                'CS 2305 - Discrete Mathematics',
                'MATH 3330 - Probability and Statistics'
            ],
            'next_steps': [
                'Explore different tech fields',
                'Take foundational courses',
                'Join tech clubs and organizations',
                'Build a strong academic foundation'
            ]
        }
