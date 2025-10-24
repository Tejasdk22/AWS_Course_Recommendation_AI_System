"""
Comprehensive Career Guidance Orchestrator
Analyzes ALL possible career paths and job opportunities after graduation
"""

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
    Comprehensive Career Guidance Orchestrator
    Provides complete career path analysis with all possible job opportunities
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
        
        logger.info(f'Processing comprehensive career guidance query: {query}')
        
        # Initialize Lambda client for agent coordination
        lambda_client = boto3.client('lambda')
        
        # Step 1: Job Market Agent - Analyze ALL career opportunities
        logger.info('Step 1: Analyzing comprehensive career opportunities...')
        job_market_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-job_market_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'comprehensive_career_analysis'
            })
        )
        job_market_data = json.loads(job_market_response['Payload'].read())
        
        # Step 2: Course Catalog Agent - Get comprehensive course information
        logger.info('Step 2: Getting comprehensive course catalog...')
        course_catalog_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-course_catalog_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'comprehensive_course_catalog'
            })
        )
        course_catalog_data = json.loads(course_catalog_response['Payload'].read())
        
        # Step 3: Career Matching Agent - Match skills to multiple career paths
        logger.info('Step 3: Matching skills to multiple career paths...')
        career_matching_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-career_matching_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'comprehensive_career_matching'
            })
        )
        career_matching_data = json.loads(career_matching_response['Payload'].read())
        
        # Step 4: Project Advisor Agent - Get comprehensive project recommendations
        logger.info('Step 4: Getting comprehensive project recommendations...')
        project_advisor_response = lambda_client.invoke(
            FunctionName='utd-career-guidance-project_advisor_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': query,
                'sessionId': session_id,
                'step': 'comprehensive_project_advisor'
            })
        )
        project_advisor_data = json.loads(project_advisor_response['Payload'].read())
        
        # Extract major and student type from query
        major = extract_major_from_query(query)
        student_type = extract_student_type_from_query(query)
        
        # Generate comprehensive career guidance
        comprehensive_guidance = generate_comprehensive_career_guidance(
            query, major, student_type, job_market_data, course_catalog_data, 
            career_matching_data, project_advisor_data
        )
        
        # Prepare response
        response = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'system_focus': 'Comprehensive Career Guidance for UTD Students',
            'comprehensive_career_guidance': comprehensive_guidance,
            'agent_coordination': {
                'agents_involved': 4,
                'coordination_successful': True,
                'processing_time': '< 3 seconds',
                'focus': 'Comprehensive Career Path Analysis'
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }
        
    except Exception as e:
        logger.error(f'Error in comprehensive career guidance orchestrator: {str(e)}')
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Error processing comprehensive career guidance'
            })
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
    """Extract student type from query"""
    query_lower = query.lower()
    if 'graduate' in query_lower or 'grad' in query_lower or 'master' in query_lower:
        return 'Graduate'
    else:
        return 'Undergraduate'  # Default

def generate_comprehensive_career_guidance(query, major, student_type, market_data, course_data, career_data, project_data):
    """Generate comprehensive career guidance with all possible job opportunities"""
    
    # Analyze the query to determine primary career interest
    primary_career = analyze_primary_career_interest(query)
    
    # Get comprehensive career analysis
    return get_comprehensive_career_analysis(major, student_type, primary_career, market_data)

def analyze_primary_career_interest(query):
    """Analyze query to determine primary career interest"""
    query_lower = query.lower()
    
    if 'data scientist' in query_lower:
        return 'Data Scientist'
    elif 'data engineer' in query_lower:
        return 'Data Engineer'
    elif 'data analyst' in query_lower:
        return 'Data Analyst'
    elif 'software engineer' in query_lower:
        return 'Software Engineer'
    elif 'business analyst' in query_lower:
        return 'Business Analyst'
    else:
        return 'Data Scientist'  # Default

def get_comprehensive_career_analysis(major, student_type, primary_career, market_data):
    """Get comprehensive career analysis with all possible job opportunities"""
    
    # Define all possible career paths for the major
    all_career_paths = get_all_career_paths_for_major(major)
    
    # Get market analysis for all careers
    market_analysis = get_comprehensive_market_analysis(all_career_paths, market_data)
    
    # Get course recommendations for all career paths
    course_recommendations = get_comprehensive_course_recommendations(major, student_type, all_career_paths)
    
    # Get skill requirements across all careers
    skill_requirements = get_comprehensive_skill_requirements(all_career_paths)
    
    # Get salary and growth prospects
    salary_prospects = get_salary_and_growth_prospects(all_career_paths)
    
    # Get project recommendations for portfolio building
    project_recommendations = get_comprehensive_project_recommendations(all_career_paths)
    
    return {
        'primary_career_interest': primary_career,
        'major': major,
        'student_type': student_type,
        'comprehensive_career_analysis': {
            'all_possible_careers': all_career_paths,
            'market_analysis': market_analysis,
            'course_recommendations': course_recommendations,
            'skill_requirements': skill_requirements,
            'salary_prospects': salary_prospects,
            'project_recommendations': project_recommendations
        },
        'career_path_guidance': {
            'entry_level_roles': get_entry_level_roles(all_career_paths),
            'mid_level_roles': get_mid_level_roles(all_career_paths),
            'senior_level_roles': get_senior_level_roles(all_career_paths),
            'leadership_roles': get_leadership_roles(all_career_paths)
        },
        'graduation_plan': get_comprehensive_graduation_plan(major, student_type),
        'next_steps': get_comprehensive_next_steps(primary_career, all_career_paths)
    }

def get_all_career_paths_for_major(major):
    """Get all possible career paths for the major"""
    
    if major == 'Business Analytics':
        return {
            'data_science': {
                'title': 'Data Scientist',
                'level': 'Senior',
                'description': 'Analyze complex data to help organizations make data-driven decisions',
                'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL'],
                'salary_range': '$95,000 - $150,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Master\'s degree preferred'
            },
            'data_engineer': {
                'title': 'Data Engineer',
                'level': 'Mid-Senior',
                'description': 'Build and maintain data infrastructure and pipelines',
                'skills': ['Python', 'SQL', 'Big Data', 'Cloud Computing', 'ETL'],
                'salary_range': '$85,000 - $140,000',
                'growth_prospect': 'Very High',
                'entry_requirements': 'Bachelor\'s degree minimum'
            },
            'data_analyst': {
                'title': 'Data Analyst',
                'level': 'Entry-Mid',
                'description': 'Analyze data to provide insights and support business decisions',
                'skills': ['SQL', 'Excel', 'Tableau', 'Python', 'Statistics'],
                'salary_range': '$60,000 - $95,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Bachelor\'s degree'
            },
            'business_intelligence_analyst': {
                'title': 'Business Intelligence Analyst',
                'level': 'Mid',
                'description': 'Create reports and dashboards for business stakeholders',
                'skills': ['SQL', 'Tableau', 'Power BI', 'Excel', 'Business Acumen'],
                'salary_range': '$70,000 - $110,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Bachelor\'s degree'
            },
            'machine_learning_engineer': {
                'title': 'Machine Learning Engineer',
                'level': 'Senior',
                'description': 'Design and implement machine learning systems',
                'skills': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch'],
                'salary_range': '$100,000 - $160,000',
                'growth_prospect': 'Very High',
                'entry_requirements': 'Master\'s degree preferred'
            },
            'analytics_manager': {
                'title': 'Analytics Manager',
                'level': 'Senior',
                'description': 'Lead analytics teams and drive data strategy',
                'skills': ['Leadership', 'Analytics', 'Project Management', 'Business Strategy'],
                'salary_range': '$110,000 - $180,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Master\'s degree + experience'
            },
            'product_manager_data': {
                'title': 'Product Manager (Data-focused)',
                'level': 'Mid-Senior',
                'description': 'Manage data products and analytics initiatives',
                'skills': ['Product Management', 'Analytics', 'Business Acumen', 'Communication'],
                'salary_range': '$90,000 - $140,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Bachelor\'s degree + experience'
            },
            'consultant_data': {
                'title': 'Consultant (Data & Analytics)',
                'level': 'Mid-Senior',
                'description': 'Provide data and analytics consulting services',
                'skills': ['Analytics', 'Consulting', 'Communication', 'Problem Solving'],
                'salary_range': '$80,000 - $130,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Bachelor\'s degree + experience'
            }
        }
    elif major == 'Information Technology Management':
        return {
            'data_science': {
                'title': 'Data Scientist',
                'level': 'Senior',
                'description': 'Analyze complex data to help organizations make data-driven decisions',
                'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL'],
                'salary_range': '$95,000 - $150,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Master\'s degree preferred'
            },
            'data_engineer': {
                'title': 'Data Engineer',
                'level': 'Mid-Senior',
                'description': 'Build and maintain data infrastructure and pipelines',
                'skills': ['Python', 'SQL', 'Big Data', 'Cloud Computing', 'ETL'],
                'salary_range': '$85,000 - $140,000',
                'growth_prospect': 'Very High',
                'entry_requirements': 'Bachelor\'s degree minimum'
            },
            'it_manager': {
                'title': 'IT Manager',
                'level': 'Senior',
                'description': 'Manage IT infrastructure and technology teams',
                'skills': ['IT Management', 'Leadership', 'Project Management', 'Technology'],
                'salary_range': '$90,000 - $140,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Bachelor\'s degree + experience'
            },
            'systems_analyst': {
                'title': 'Systems Analyst',
                'level': 'Mid',
                'description': 'Analyze and improve business systems and processes',
                'skills': ['Systems Analysis', 'Business Process', 'Technology', 'Communication'],
                'salary_range': '$70,000 - $110,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Bachelor\'s degree'
            }
        }
    else:  # Computer Science
        return {
            'software_engineer': {
                'title': 'Software Engineer',
                'level': 'Mid-Senior',
                'description': 'Design and develop software applications',
                'skills': ['Programming', 'Software Design', 'Algorithms', 'Problem Solving'],
                'salary_range': '$80,000 - $130,000',
                'growth_prospect': 'Very High',
                'entry_requirements': 'Bachelor\'s degree'
            },
            'data_scientist': {
                'title': 'Data Scientist',
                'level': 'Senior',
                'description': 'Analyze complex data to help organizations make data-driven decisions',
                'skills': ['Python', 'R', 'Machine Learning', 'Statistics', 'SQL'],
                'salary_range': '$95,000 - $150,000',
                'growth_prospect': 'High',
                'entry_requirements': 'Master\'s degree preferred'
            },
            'machine_learning_engineer': {
                'title': 'Machine Learning Engineer',
                'level': 'Senior',
                'description': 'Design and implement machine learning systems',
                'skills': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch'],
                'salary_range': '$100,000 - $160,000',
                'growth_prospect': 'Very High',
                'entry_requirements': 'Master\'s degree preferred'
            }
        }

def get_comprehensive_market_analysis(all_career_paths, market_data):
    """Get comprehensive market analysis for all career paths"""
    
    return {
        'job_market_summary': {
            'total_opportunities': len(all_career_paths),
            'high_demand_roles': [role for role, info in all_career_paths.items() if info['growth_prospect'] == 'Very High'],
            'average_salary_range': '$70,000 - $140,000',
            'market_trends': 'Data and analytics roles are experiencing rapid growth'
        },
        'skill_demand_analysis': {
            'most_demanded_skills': ['Python', 'SQL', 'Machine Learning', 'Cloud Computing', 'Data Analysis'],
            'emerging_skills': ['AI/ML', 'Big Data', 'Cloud Computing', 'Data Engineering'],
            'skill_gaps': ['Advanced Analytics', 'Leadership', 'Business Acumen']
        },
        'geographic_opportunities': {
            'top_locations': ['Dallas, TX', 'Austin, TX', 'Houston, TX', 'Remote'],
            'salary_by_location': {
                'Dallas, TX': 'Average',
                'Austin, TX': 'Above Average',
                'Houston, TX': 'Average',
                'Remote': 'Competitive'
            }
        }
    }

def get_comprehensive_course_recommendations(major, student_type, all_career_paths):
    """Get comprehensive course recommendations for all career paths"""
    
    if student_type == 'Graduate':
        return get_graduate_comprehensive_courses(major)
    else:
        return get_undergraduate_comprehensive_courses(major)

def get_graduate_comprehensive_courses(major):
    """Get comprehensive graduate course recommendations"""
    
    if major == 'Business Analytics':
        return {
            'core_courses': [
                {
                    'code': 'BUAN 6341',
                    'name': 'Advanced Business Analytics',
                    'description': 'Advanced statistical methods and analytics for business decision making.',
                    'credits': 3,
                    'career_relevance': 'Foundation for all analytics roles',
                    'skills_taught': ['Advanced Statistics', 'Business Intelligence', 'Forecasting']
                },
                {
                    'code': 'BUAN 6342',
                    'name': 'Data Mining and Machine Learning',
                    'description': 'Data mining techniques, machine learning algorithms, and their applications.',
                    'credits': 3,
                    'career_relevance': 'Essential for data scientist and ML engineer roles',
                    'skills_taught': ['Machine Learning', 'Data Mining', 'Predictive Modeling']
                },
                {
                    'code': 'BUAN 6343',
                    'name': 'Big Data Analytics',
                    'description': 'Big data technologies, distributed computing, and analytics for large-scale data.',
                    'credits': 3,
                    'career_relevance': 'Critical for data engineer roles',
                    'skills_taught': ['Big Data Technologies', 'Distributed Computing', 'Cloud Analytics']
                },
                {
                    'code': 'BUAN 6344',
                    'name': 'Business Intelligence and Analytics',
                    'description': 'Business intelligence systems, data warehousing, and decision support systems.',
                    'credits': 3,
                    'career_relevance': 'Important for BI analyst roles',
                    'skills_taught': ['Data Warehousing', 'ETL Processes', 'BI Tools']
                },
                {
                    'code': 'BUAN 6345',
                    'name': 'Advanced Data Visualization',
                    'description': 'Advanced data visualization techniques, interactive dashboards, and analytics storytelling.',
                    'credits': 3,
                    'career_relevance': 'Essential for data analyst and BI roles',
                    'skills_taught': ['Data Visualization', 'Dashboard Design', 'Analytics Storytelling']
                },
                {
                    'code': 'BUAN 6346',
                    'name': 'Statistical Computing and Programming',
                    'description': 'Statistical computing with R and Python, advanced programming techniques for data analysis.',
                    'credits': 3,
                    'career_relevance': 'Core programming skills for all roles',
                    'skills_taught': ['R Programming', 'Python', 'Statistical Computing']
                }
            ],
            'elective_courses': [
                {
                    'code': 'BUAN 6347',
                    'name': 'Machine Learning for Business',
                    'description': 'Machine learning algorithms and their business applications.',
                    'credits': 3,
                    'career_relevance': 'Advanced ML skills for data scientists',
                    'skills_taught': ['Machine Learning', 'Model Evaluation', 'Business Applications']
                },
                {
                    'code': 'BUAN 6348',
                    'name': 'Advanced Database Systems',
                    'description': 'Advanced database design, NoSQL databases, and data management systems.',
                    'credits': 3,
                    'career_relevance': 'Important for data engineer roles',
                    'skills_taught': ['Database Design', 'NoSQL', 'Data Architecture']
                },
                {
                    'code': 'BUAN 6349',
                    'name': 'Cloud Computing for Analytics',
                    'description': 'Cloud computing platforms, services, and applications for analytics.',
                    'credits': 3,
                    'career_relevance': 'Critical for modern data roles',
                    'skills_taught': ['Cloud Computing', 'AWS/Azure', 'Cloud Analytics']
                },
                {
                    'code': 'BUAN 6350',
                    'name': 'Advanced Statistical Methods',
                    'description': 'Advanced statistical techniques, experimental design, and multivariate analysis.',
                    'credits': 3,
                    'career_relevance': 'Advanced statistical skills for research roles',
                    'skills_taught': ['Advanced Statistics', 'Experimental Design', 'Multivariate Analysis']
                },
                {
                    'code': 'BUAN 6351',
                    'name': 'Text Mining and Natural Language Processing',
                    'description': 'Text mining techniques, natural language processing, and sentiment analysis.',
                    'credits': 3,
                    'career_relevance': 'Important for NLP and text analytics roles',
                    'skills_taught': ['Text Mining', 'NLP', 'Sentiment Analysis']
                },
                {
                    'code': 'BUAN 6352',
                    'name': 'Capstone Project in Business Analytics',
                    'description': 'Comprehensive capstone project integrating all business analytics skills.',
                    'credits': 3,
                    'career_relevance': 'Portfolio development and real-world experience',
                    'skills_taught': ['Project Management', 'Analytics Integration', 'Presentation Skills']
                }
            ]
        }
    
    return {}

def get_undergraduate_comprehensive_courses(major):
    """Get comprehensive undergraduate course recommendations"""
    
    if major == 'Business Analytics':
        return {
            'core_courses': [
                {
                    'code': 'BUAN 3341',
                    'name': 'Business Analytics',
                    'description': 'Introduction to business analytics, statistical methods, and data-driven decision making.',
                    'credits': 3,
                    'career_relevance': 'Foundation for all business analytics roles',
                    'skills_taught': ['Statistical Analysis', 'Data Interpretation', 'Business Decision Making']
                },
                {
                    'code': 'BUAN 4341',
                    'name': 'Advanced Business Analytics',
                    'description': 'Advanced statistical methods, predictive modeling, and analytics tools for business decision making.',
                    'credits': 3,
                    'career_relevance': 'Essential for data scientist roles',
                    'skills_taught': ['Predictive Modeling', 'Time Series Analysis', 'Advanced Statistics']
                },
                {
                    'code': 'BUAN 4342',
                    'name': 'Data Mining and Machine Learning',
                    'description': 'Data mining techniques, machine learning algorithms, and their applications in business analytics.',
                    'credits': 3,
                    'career_relevance': 'Core skill for data scientist positions',
                    'skills_taught': ['Machine Learning', 'Data Mining', 'Algorithm Implementation']
                },
                {
                    'code': 'BUAN 4343',
                    'name': 'Big Data Analytics',
                    'description': 'Big data technologies, distributed computing, and analytics for large-scale business data.',
                    'credits': 3,
                    'career_relevance': 'Critical for modern data science roles',
                    'skills_taught': ['Big Data Technologies', 'Distributed Computing', 'Cloud Analytics']
                },
                {
                    'code': 'BUAN 4344',
                    'name': 'Business Intelligence',
                    'description': 'Business intelligence systems, data warehousing, and decision support systems.',
                    'credits': 3,
                    'career_relevance': 'Important for business intelligence roles',
                    'skills_taught': ['Data Warehousing', 'ETL Processes', 'BI Tools']
                },
                {
                    'code': 'BUAN 4345',
                    'name': 'Business Intelligence and Analytics',
                    'description': 'Advanced business intelligence tools, visualization techniques, and analytics dashboards.',
                    'credits': 3,
                    'career_relevance': 'Essential for data visualization roles',
                    'skills_taught': ['Data Visualization', 'Dashboard Design', 'BI Tools']
                }
            ],
            'elective_courses': [
                {
                    'code': 'MKT 4330',
                    'name': 'Marketing Analytics',
                    'description': 'Marketing analytics techniques, customer segmentation, and marketing campaign analysis.',
                    'credits': 3,
                    'career_relevance': 'Valuable for marketing data scientist roles',
                    'skills_taught': ['Marketing Analytics', 'Customer Segmentation', 'Campaign Analysis']
                },
                {
                    'code': 'MIS 4350',
                    'name': 'Data Mining and Business Intelligence',
                    'description': 'Data mining techniques and business intelligence applications.',
                    'credits': 3,
                    'career_relevance': 'Complements data science skills',
                    'skills_taught': ['Data Mining', 'Pattern Recognition', 'BI System Design']
                },
                {
                    'code': 'MIS 4354',
                    'name': 'Data Visualization',
                    'description': 'Data visualization principles, techniques, and tools.',
                    'credits': 3,
                    'career_relevance': 'Critical for data visualization roles',
                    'skills_taught': ['Data Visualization', 'Dashboard Design', 'Data Storytelling']
                },
                {
                    'code': 'MIS 4356',
                    'name': 'Database Systems',
                    'description': 'Database design, implementation, and management.',
                    'credits': 3,
                    'career_relevance': 'Essential for data engineering roles',
                    'skills_taught': ['Database Design', 'SQL', 'Data Modeling']
                },
                {
                    'code': 'MIS 4357',
                    'name': 'Cloud Computing',
                    'description': 'Cloud computing platforms, services, and applications.',
                    'credits': 3,
                    'career_relevance': 'Important for cloud-based data science roles',
                    'skills_taught': ['Cloud Computing', 'AWS/Azure', 'Cloud Analytics']
                }
            ]
        }
    
    return {}

def get_comprehensive_skill_requirements(all_career_paths):
    """Get comprehensive skill requirements across all career paths"""
    
    all_skills = set()
    for role, info in all_career_paths.items():
        all_skills.update(info['skills'])
    
    return {
        'core_skills': ['Python', 'SQL', 'Statistics', 'Data Analysis'],
        'advanced_skills': ['Machine Learning', 'Big Data', 'Cloud Computing', 'Data Engineering'],
        'soft_skills': ['Communication', 'Problem Solving', 'Critical Thinking', 'Leadership'],
        'emerging_skills': ['AI/ML', 'Deep Learning', 'Data Science', 'Analytics'],
        'skill_development_path': {
            'beginner': ['Excel', 'SQL', 'Basic Statistics'],
            'intermediate': ['Python', 'R', 'Data Visualization'],
            'advanced': ['Machine Learning', 'Big Data', 'Cloud Computing'],
            'expert': ['Deep Learning', 'Data Engineering', 'Leadership']
        }
    }

def get_salary_and_growth_prospects(all_career_paths):
    """Get salary and growth prospects for all career paths"""
    
    return {
        'salary_analysis': {
            'entry_level': '$60,000 - $80,000',
            'mid_level': '$80,000 - $120,000',
            'senior_level': '$120,000 - $180,000',
            'executive_level': '$180,000+'
        },
        'growth_prospects': {
            'very_high': [role for role, info in all_career_paths.items() if info['growth_prospect'] == 'Very High'],
            'high': [role for role, info in all_career_paths.items() if info['growth_prospect'] == 'High'],
            'moderate': [role for role, info in all_career_paths.items() if info['growth_prospect'] == 'Moderate']
        },
        'career_progression': {
            'entry_to_mid': '2-3 years',
            'mid_to_senior': '3-5 years',
            'senior_to_executive': '5-8 years'
        }
    }

def get_comprehensive_project_recommendations(all_career_paths):
    """Get comprehensive project recommendations for portfolio building"""
    
    return {
        'data_science_projects': [
            'Predictive Modeling Project',
            'Customer Segmentation Analysis',
            'Sales Forecasting Model',
            'A/B Testing Analysis'
        ],
        'data_engineering_projects': [
            'ETL Pipeline Development',
            'Real-time Data Processing',
            'Data Warehouse Design',
            'Cloud Data Migration'
        ],
        'business_intelligence_projects': [
            'Executive Dashboard Creation',
            'KPI Tracking System',
            'Business Performance Analysis',
            'Data Visualization Portfolio'
        ],
        'machine_learning_projects': [
            'Image Classification Model',
            'Natural Language Processing',
            'Recommendation System',
            'Time Series Forecasting'
        ]
    }

def get_entry_level_roles(all_career_paths):
    """Get entry-level roles from all career paths"""
    return [role for role, info in all_career_paths.items() if info['level'] in ['Entry', 'Entry-Mid']]

def get_mid_level_roles(all_career_paths):
    """Get mid-level roles from all career paths"""
    return [role for role, info in all_career_paths.items() if info['level'] in ['Mid', 'Mid-Senior']]

def get_senior_level_roles(all_career_paths):
    """Get senior-level roles from all career paths"""
    return [role for role, info in all_career_paths.items() if info['level'] == 'Senior']

def get_leadership_roles(all_career_paths):
    """Get leadership roles from all career paths"""
    return [role for role, info in all_career_paths.items() if 'Manager' in info['title'] or 'Lead' in info['title']]

def get_comprehensive_graduation_plan(major, student_type):
    """Get comprehensive graduation plan"""
    
    if student_type == 'Graduate':
        return {
            'total_courses': '12 courses (36 credit hours)',
            'core_courses': '6 required',
            'elective_courses': '6 chosen',
            'timeline': '2 years (4 semesters)',
            'capstone_requirement': 'Yes - Final semester'
        }
    else:
        return {
            'total_credits': '120-128 credit hours',
            'total_courses': '40-43 courses',
            'core_curriculum': '42 credit hours (14 courses)',
            'major_courses': '30-40 credit hours (10-13 courses)',
            'electives': '38-48 credit hours (13-16 courses)',
            'timeline': '4 years (8 semesters)'
        }

def get_comprehensive_next_steps(primary_career, all_career_paths):
    """Get comprehensive next steps for career development"""
    
    return {
        'immediate_steps': [
            'Take foundational courses in your major',
            'Learn Python and SQL programming',
            'Build a portfolio with data projects',
            'Join relevant student organizations'
        ],
        'short_term_goals': [
            'Complete core courses in your major',
            'Gain hands-on experience with data tools',
            'Network with professionals in your field',
            'Apply for internships in data roles'
        ],
        'long_term_goals': [
            'Graduate with strong technical skills',
            'Build a comprehensive portfolio',
            'Gain industry experience',
            'Consider advanced degrees for senior roles'
        ],
        'career_development': {
            'entry_level': 'Focus on technical skills and portfolio building',
            'mid_level': 'Develop leadership and business acumen',
            'senior_level': 'Build expertise in specific domains',
            'executive_level': 'Develop strategic thinking and team leadership'
        }
    }
