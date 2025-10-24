"""
AWS Lambda function for ProjectAdvisorAgent in Bedrock AgentCore
Autonomous project suggestion and portfolio development agent
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime
import requests

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for ProjectAdvisorAgent
    Processes project advice requests autonomously
    """
    
    try:
        # Extract query from event
        query = event.get('query', '')
        session_id = event.get('sessionId', '')
        
        print(f"ProjectAdvisorAgent processing query: {query}")
        
        # Initialize agent
        agent = ProjectAdvisorAgent()
        
        # Process the query autonomously
        result = agent.process_project_advice_query(query)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'ProjectAdvisorAgent',
                'query': query,
                'result': result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in ProjectAdvisorAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'ProjectAdvisorAgent'
            }
        }

class ProjectAdvisorAgent:
    """Autonomous Project Advisor Agent"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'utd-career-guidance-data'
        self.lambda_client = boto3.client('lambda')
        
    def process_project_advice_query(self, query: str) -> Dict[str, Any]:
        """Process project advice query autonomously"""
        
        # Extract career goals and skills from query
        career_goals = self._extract_career_goals(query)
        
        # Get career matching data to understand skill gaps
        career_matching_data = self._get_career_matching_data(career_goals)
        
        # Generate project recommendations
        project_recommendations = self._generate_project_recommendations(career_goals, career_matching_data)
        
        # Create portfolio development plan
        portfolio_plan = self._create_portfolio_plan(project_recommendations, career_goals)
        
        return {
            'career_goals': career_goals,
            'career_matching_data': career_matching_data,
            'project_recommendations': project_recommendations,
            'portfolio_plan': portfolio_plan,
            'processed_at': datetime.now().isoformat()
        }
    
    def _extract_career_goals(self, query: str) -> List[str]:
        """Extract career goals from query"""
        goals = []
        
        # Common career goals
        career_terms = [
            'data scientist', 'software engineer', 'data analyst',
            'machine learning engineer', 'product manager', 'consultant',
            'developer', 'analyst', 'engineer', 'manager', 'researcher',
            'architect', 'director', 'specialist', 'coordinator'
        ]
        
        query_lower = query.lower()
        for term in career_terms:
            if term in query_lower:
                goals.append(term)
        
        return goals if goals else ['data scientist']  # Default
    
    def _get_career_matching_data(self, career_goals: List[str]) -> Dict[str, Any]:
        """Get career matching data from CareerMatchingAgent"""
        try:
            # Invoke CareerMatchingAgent Lambda function
            response = self.lambda_client.invoke(
                FunctionName='utd-career-guidance-career_matching_agent',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': ' '.join(career_goals),
                    'sessionId': f"project-advice-{datetime.now().timestamp()}"
                })
            )
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                return result['body']['result']
            else:
                return {'error': 'Failed to get career matching data'}
                
        except Exception as e:
            print(f"Error getting career matching data: {e}")
            return {'error': str(e)}
    
    def _generate_project_recommendations(self, career_goals: List[str], 
                                        career_matching_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate project recommendations based on career goals, major, and skill gaps"""
        
        projects = []
        
        # Extract major from career goals (if mentioned)
        major = self._extract_major_from_goals(career_goals)
        
        # Extract skill gaps from career matching data
        skill_gaps = []
        if 'matching_analysis' in career_matching_data and 'skill_gaps' in career_matching_data['matching_analysis']:
            skill_gaps = career_matching_data['matching_analysis']['skill_gaps']
        
        # Generate projects based on career goals and major
        for goal in career_goals:
            if 'data scientist' in goal.lower():
                projects.extend(self._get_data_science_projects(skill_gaps, major))
            elif 'software engineer' in goal.lower() or 'developer' in goal.lower():
                projects.extend(self._get_software_engineering_projects(skill_gaps, major))
            elif 'machine learning' in goal.lower():
                projects.extend(self._get_ml_engineering_projects(skill_gaps, major))
            elif 'data analyst' in goal.lower():
                projects.extend(self._get_data_analysis_projects(skill_gaps, major))
            elif 'business analyst' in goal.lower():
                projects.extend(self._get_business_analytics_projects(skill_gaps, major))
            elif 'product manager' in goal.lower():
                projects.extend(self._get_product_management_projects(skill_gaps, major))
            elif 'consultant' in goal.lower():
                projects.extend(self._get_consulting_projects(skill_gaps, major))
            else:
                projects.extend(self._get_general_projects(skill_gaps, major))
        
        # Remove duplicates and limit to top 5
        unique_projects = []
        seen_titles = set()
        for project in projects:
            if project['title'] not in seen_titles:
                unique_projects.append(project)
                seen_titles.add(project['title'])
                if len(unique_projects) >= 5:
                    break
        
        return unique_projects
    
    def _extract_major_from_goals(self, career_goals: List[str]) -> str:
        """Extract major from career goals"""
        goals_text = ' '.join(career_goals).lower()
        
        if 'business analytics' in goals_text or 'ba' in goals_text:
            return 'Business Analytics'
        elif 'information technology' in goals_text or 'itm' in goals_text:
            return 'Information Technology Management'
        elif 'computer science' in goals_text or 'cs' in goals_text:
            return 'Computer Science'
        elif 'data science' in goals_text:
            return 'Data Science'
        else:
            return 'Business Analytics'  # Default
    
    def _get_data_science_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get data science project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Business Intelligence Dashboard',
                    'description': 'Create an interactive BI dashboard using Tableau/Power BI to analyze business metrics and KPIs from real company data',
                    'technologies': ['Tableau', 'Power BI', 'SQL', 'Excel', 'Python', 'Pandas'],
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'skills_developed': ['Business Intelligence', 'Data Visualization', 'SQL', 'Business Analysis'],
                    'github_template': 'https://github.com/example/business-intelligence-dashboard',
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
                    'github_template': 'https://github.com/example/customer-segmentation',
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
                    'github_template': 'https://github.com/example/sales-forecasting',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Excellent for BA students - directly applicable to business'
                }
            ]
        elif major == 'Information Technology Management':
            return [
                {
                    'title': 'Data Pipeline for Business Intelligence',
                    'description': 'Build an ETL pipeline to process business data and feed it into a BI dashboard using cloud technologies',
                    'technologies': ['Python', 'Apache Airflow', 'AWS S3', 'PostgreSQL', 'Docker', 'Tableau'],
                    'difficulty': 'Advanced',
                    'duration': '6-8 weeks',
                    'skills_developed': ['ETL', 'Cloud Computing', 'Data Engineering', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/data-pipeline-bi',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Perfect for ITM students - combines IT infrastructure with analytics'
                },
                {
                    'title': 'Machine Learning API Service',
                    'description': 'Create a REST API service for machine learning models with proper deployment and monitoring',
                    'technologies': ['Python', 'FastAPI', 'Docker', 'AWS', 'MLflow', 'PostgreSQL'],
                    'difficulty': 'Advanced',
                    'duration': '5-7 weeks',
                    'skills_developed': ['API Development', 'MLOps', 'Cloud Computing', 'System Design'],
                    'github_template': 'https://github.com/example/ml-api-service',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Great for ITM students - focuses on technical implementation'
                }
            ]
        elif major == 'Computer Science':
            return [
                {
                    'title': 'Advanced ML Model Pipeline',
                    'description': 'Create a sophisticated ML pipeline with automated feature engineering, model selection, and deployment',
                    'technologies': ['Python', 'Scikit-learn', 'Pandas', 'Docker', 'AWS', 'MLflow', 'Kubernetes'],
                    'difficulty': 'Advanced',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Machine Learning', 'Python', 'AWS', 'Docker', 'MLOps', 'System Design'],
                    'github_template': 'https://github.com/example/advanced-ml-pipeline',
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
                    'github_template': 'https://github.com/example/streaming-data-pipeline',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Excellent for CS students - complex system design'
                }
            ]
        else:
            # Default data science projects
            return [
                {
                    'title': 'Predictive Analytics Dashboard',
                    'description': 'Build a comprehensive dashboard using Python, Pandas, and Streamlit to analyze and predict trends from real-world datasets',
                    'technologies': ['Python', 'Pandas', 'NumPy', 'Streamlit', 'Plotly', 'Scikit-learn'],
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'skills_developed': ['Data Analysis', 'Python', 'Machine Learning', 'Data Visualization'],
                    'github_template': 'https://github.com/example/data-science-dashboard',
                    'portfolio_value': 'High'
                }
            ]
    
    def _get_software_engineering_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get software engineering project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Business Analytics Web Application',
                    'description': 'Build a web app for business analytics with data visualization, reporting, and dashboard features',
                    'technologies': ['Python', 'Flask', 'React', 'PostgreSQL', 'Chart.js', 'Bootstrap'],
                    'difficulty': 'Intermediate',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Web Development', 'Python', 'Data Visualization', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/business-analytics-webapp',
                    'portfolio_value': 'High',
                    'major_specific': 'Perfect for BA students - combines web dev with business analytics'
                },
                {
                    'title': 'API for Business Intelligence',
                    'description': 'Create REST APIs for business data analysis and integrate with BI tools like Tableau',
                    'technologies': ['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'Tableau', 'AWS'],
                    'difficulty': 'Advanced',
                    'duration': '5-7 weeks',
                    'skills_developed': ['API Development', 'Python', 'Database Design', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/bi-api',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Great for BA students - focuses on business data integration'
                }
            ]
        elif major == 'Information Technology Management':
            return [
                {
                    'title': 'Enterprise Software System',
                    'description': 'Build a comprehensive enterprise application with user management, reporting, and integration capabilities',
                    'technologies': ['Java', 'Spring Boot', 'React', 'PostgreSQL', 'Docker', 'AWS'],
                    'difficulty': 'Advanced',
                    'duration': '8-10 weeks',
                    'skills_developed': ['Enterprise Development', 'Java', 'System Design', 'Cloud Computing'],
                    'github_template': 'https://github.com/example/enterprise-system',
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
                    'github_template': 'https://github.com/example/cloud-native-app',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Excellent for ITM students - modern cloud technologies'
                }
            ]
        elif major == 'Computer Science':
            return [
                {
                    'title': 'Full-Stack Web Application',
                    'description': 'Build a complete web application with React frontend, Node.js backend, and database integration',
                    'technologies': ['React', 'Node.js', 'Express', 'MongoDB', 'JavaScript', 'CSS'],
                    'difficulty': 'Intermediate',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Web Development', 'JavaScript', 'React', 'Node.js', 'Database Design'],
                    'github_template': 'https://github.com/example/fullstack-app',
                    'portfolio_value': 'High',
                    'major_specific': 'Great for CS students - full-stack development'
                },
                {
                    'title': 'Microservices Architecture',
                    'description': 'Design and implement a microservices-based system with API gateway, service discovery, and containerization',
                    'technologies': ['Docker', 'Kubernetes', 'Node.js', 'MongoDB', 'Redis', 'Nginx'],
                    'difficulty': 'Advanced',
                    'duration': '10-12 weeks',
                    'skills_developed': ['Microservices', 'Docker', 'Kubernetes', 'System Design'],
                    'github_template': 'https://github.com/example/microservices-system',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Perfect for CS students - advanced system design'
                }
            ]
        else:
            # Default software engineering projects
            return [
                {
                    'title': 'Full-Stack Web Application',
                    'description': 'Build a complete web application with React frontend, Node.js backend, and database integration',
                    'technologies': ['React', 'Node.js', 'Express', 'MongoDB', 'JavaScript', 'CSS'],
                    'difficulty': 'Intermediate',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Web Development', 'JavaScript', 'React', 'Node.js', 'Database Design'],
                    'github_template': 'https://github.com/example/fullstack-app',
                    'portfolio_value': 'High'
                }
            ]
    
    def _get_ml_engineering_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get machine learning engineering project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Business ML Model Pipeline',
                    'description': 'Create an end-to-end ML pipeline for business predictions with automated retraining and monitoring',
                    'technologies': ['Python', 'Scikit-learn', 'Pandas', 'Docker', 'AWS', 'MLflow', 'Tableau'],
                    'difficulty': 'Advanced',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Machine Learning', 'Python', 'Business Intelligence', 'MLOps'],
                    'github_template': 'https://github.com/example/business-ml-pipeline',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Perfect for BA students - business-focused ML'
                }
            ]
        elif major == 'Information Technology Management':
            return [
                {
                    'title': 'ML Model Deployment Platform',
                    'description': 'Create a platform for deploying, monitoring, and managing machine learning models in production',
                    'technologies': ['Python', 'FastAPI', 'Docker', 'Kubernetes', 'Prometheus', 'Grafana'],
                    'difficulty': 'Advanced',
                    'duration': '8-10 weeks',
                    'skills_developed': ['MLOps', 'Python', 'Docker', 'Kubernetes', 'System Design'],
                    'github_template': 'https://github.com/example/ml-deployment-platform',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Great for ITM students - infrastructure focus'
                }
            ]
        else:
            return [
                {
                    'title': 'ML Model Deployment Platform',
                    'description': 'Create a platform for deploying, monitoring, and managing machine learning models in production',
                    'technologies': ['Python', 'FastAPI', 'Docker', 'Kubernetes', 'Prometheus', 'Grafana'],
                    'difficulty': 'Advanced',
                    'duration': '8-10 weeks',
                    'skills_developed': ['MLOps', 'Python', 'Docker', 'Kubernetes', 'System Design'],
                    'github_template': 'https://github.com/example/ml-deployment-platform',
                    'portfolio_value': 'Very High'
                }
            ]
    
    def _get_data_analysis_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get data analysis project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Business Intelligence Dashboard',
                    'description': 'Create interactive dashboards for business metrics using Tableau/Power BI and SQL',
                    'technologies': ['SQL', 'Tableau', 'Power BI', 'Python', 'Pandas', 'PostgreSQL'],
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'skills_developed': ['Data Analysis', 'SQL', 'Data Visualization', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/bi-dashboard',
                    'portfolio_value': 'High',
                    'major_specific': 'Perfect for BA students - business-focused analytics'
                },
                {
                    'title': 'Customer Analytics Project',
                    'description': 'Analyze customer behavior and create actionable insights for business decision-making',
                    'technologies': ['Python', 'Pandas', 'Matplotlib', 'Seaborn', 'SQL', 'Jupyter'],
                    'difficulty': 'Intermediate',
                    'duration': '3-4 weeks',
                    'skills_developed': ['Data Analysis', 'Python', 'Customer Analytics', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/customer-analytics',
                    'portfolio_value': 'High',
                    'major_specific': 'Great for BA students - practical business application'
                }
            ]
        elif major == 'Information Technology Management':
            return [
                {
                    'title': 'IT Performance Analytics Dashboard',
                    'description': 'Create dashboards to analyze IT system performance, user behavior, and operational metrics',
                    'technologies': ['Python', 'Streamlit', 'PostgreSQL', 'Docker', 'AWS', 'Grafana'],
                    'difficulty': 'Intermediate',
                    'duration': '5-6 weeks',
                    'skills_developed': ['Data Analysis', 'Python', 'IT Analytics', 'System Monitoring'],
                    'github_template': 'https://github.com/example/it-performance-dashboard',
                    'portfolio_value': 'High',
                    'major_specific': 'Perfect for ITM students - IT-focused analytics'
                }
            ]
        else:
            return [
                {
                    'title': 'Business Intelligence Dashboard',
                    'description': 'Create interactive dashboards for business metrics using Tableau/Power BI and SQL',
                    'technologies': ['SQL', 'Tableau', 'Python', 'Pandas', 'PostgreSQL'],
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'skills_developed': ['Data Analysis', 'SQL', 'Data Visualization', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/bi-dashboard',
                    'portfolio_value': 'High'
                }
            ]
    
    def _get_business_analytics_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get business analytics project recommendations"""
        return [
            {
                'title': 'Market Research Analysis',
                'description': 'Conduct comprehensive market research analysis with data collection, analysis, and visualization',
                'technologies': ['Python', 'Pandas', 'Tableau', 'SQL', 'Excel', 'Survey Tools'],
                'difficulty': 'Intermediate',
                'duration': '4-5 weeks',
                'skills_developed': ['Market Research', 'Data Analysis', 'Python', 'Business Intelligence'],
                'github_template': 'https://github.com/example/market-research-analysis',
                'portfolio_value': 'High',
                'major_specific': 'Perfect for BA students - market research focus'
            },
            {
                'title': 'Financial Analytics Dashboard',
                'description': 'Build a financial analytics dashboard for tracking KPIs, revenue analysis, and forecasting',
                'technologies': ['Python', 'Streamlit', 'Pandas', 'Plotly', 'SQL', 'Excel'],
                'difficulty': 'Intermediate',
                'duration': '5-6 weeks',
                'skills_developed': ['Financial Analysis', 'Python', 'Data Visualization', 'Business Intelligence'],
                'github_template': 'https://github.com/example/financial-analytics-dashboard',
                'portfolio_value': 'High',
                'major_specific': 'Great for BA students - financial analytics'
            }
        ]
    
    def _get_product_management_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get product management project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Product Analytics Platform',
                    'description': 'Build a platform to analyze product metrics, user behavior, and A/B testing results',
                    'technologies': ['Python', 'Streamlit', 'PostgreSQL', 'Docker', 'AWS', 'Analytics APIs'],
                    'difficulty': 'Advanced',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Product Analytics', 'Python', 'A/B Testing', 'Business Intelligence'],
                    'github_template': 'https://github.com/example/product-analytics-platform',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Perfect for BA students - product analytics focus'
                }
            ]
        else:
            return [
                {
                    'title': 'Product Management Portfolio',
                    'description': 'Create a comprehensive product management portfolio with case studies and mock products',
                    'technologies': ['Figma', 'Notion', 'Miro', 'Google Analytics', 'SQL', 'Python'],
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'skills_developed': ['Product Management', 'Design Thinking', 'Analytics', 'Strategy'],
                    'github_template': 'https://github.com/example/product-management-portfolio',
                    'portfolio_value': 'High'
                }
            ]
    
    def _get_consulting_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get consulting project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Business Case Study Analysis',
                    'description': 'Create comprehensive business case studies with data analysis, recommendations, and presentations',
                    'technologies': ['Python', 'Pandas', 'Tableau', 'PowerPoint', 'Excel', 'SQL'],
                    'difficulty': 'Advanced',
                    'duration': '6-8 weeks',
                    'skills_developed': ['Business Analysis', 'Case Studies', 'Data Analysis', 'Presentation'],
                    'github_template': 'https://github.com/example/business-case-studies',
                    'portfolio_value': 'Very High',
                    'major_specific': 'Perfect for BA students - consulting case studies'
                }
            ]
        else:
            return [
                {
                    'title': 'Consulting Portfolio',
                    'description': 'Build a consulting portfolio with case studies, frameworks, and client recommendations',
                    'technologies': ['PowerPoint', 'Excel', 'Tableau', 'Python', 'SQL', 'Presentation Tools'],
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'skills_developed': ['Consulting', 'Case Studies', 'Analysis', 'Presentation'],
                    'github_template': 'https://github.com/example/consulting-portfolio',
                    'portfolio_value': 'High'
                }
            ]
    
    def _get_general_projects(self, skill_gaps: List[str], major: str) -> List[Dict[str, Any]]:
        """Get general project recommendations by major"""
        if major == 'Business Analytics':
            return [
                {
                    'title': 'Business Analytics Portfolio',
                    'description': 'Build a comprehensive portfolio showcasing business analytics projects and skills',
                    'technologies': ['Python', 'Tableau', 'Power BI', 'SQL', 'Excel', 'GitHub'],
                    'difficulty': 'Beginner',
                    'duration': '3-4 weeks',
                    'skills_developed': ['Portfolio Development', 'Business Analytics', 'Data Visualization'],
                    'github_template': 'https://github.com/example/business-analytics-portfolio',
                    'portfolio_value': 'Medium',
                    'major_specific': 'Perfect for BA students - professional portfolio'
                }
            ]
        elif major == 'Information Technology Management':
            return [
                {
                    'title': 'IT Management Portfolio',
                    'description': 'Create a portfolio showcasing IT management projects, system designs, and technical skills',
                    'technologies': ['Python', 'Docker', 'AWS', 'SQL', 'Project Management Tools', 'GitHub'],
                    'difficulty': 'Beginner',
                    'duration': '3-4 weeks',
                    'skills_developed': ['Portfolio Development', 'IT Management', 'System Design'],
                    'github_template': 'https://github.com/example/it-management-portfolio',
                    'portfolio_value': 'Medium',
                    'major_specific': 'Great for ITM students - IT management focus'
                }
            ]
        else:
            return [
                {
                    'title': 'Portfolio Website',
                    'description': 'Build a professional portfolio website showcasing your projects and skills',
                    'technologies': ['HTML', 'CSS', 'JavaScript', 'React', 'GitHub Pages'],
                    'difficulty': 'Beginner',
                    'duration': '2-3 weeks',
                    'skills_developed': ['Web Development', 'HTML', 'CSS', 'JavaScript'],
                    'github_template': 'https://github.com/example/portfolio-website',
                    'portfolio_value': 'Medium'
                }
            ]
    
    def _create_portfolio_plan(self, project_recommendations: List[Dict[str, Any]], 
                              career_goals: List[str]) -> str:
        """Create a comprehensive portfolio development plan"""
        
        plan = f"""
        **Portfolio Development Plan for: {', '.join(career_goals)}**
        
        **Recommended Projects ({len(project_recommendations)} projects):**
        """
        
        for i, project in enumerate(project_recommendations, 1):
            plan += f"""
        
        **{i}. {project['title']}**
        - **Description**: {project['description']}
        - **Technologies**: {', '.join(project['technologies'])}
        - **Difficulty**: {project['difficulty']}
        - **Duration**: {project['duration']}
        - **Skills Developed**: {', '.join(project['skills_developed'])}
        - **Portfolio Value**: {project['portfolio_value']}
        - **GitHub Template**: {project['github_template']}
        """
        
        plan += f"""
        
        **Portfolio Development Timeline:**
        
        **Phase 1 (Months 1-2): Foundation**
        - Complete 1-2 beginner/intermediate projects
        - Set up GitHub profile and portfolio website
        - Learn version control and project documentation
        
        **Phase 2 (Months 3-4): Skill Building**
        - Complete 2-3 intermediate projects
        - Focus on technologies relevant to your career goals
        - Start building a professional network
        
        **Phase 3 (Months 5-6): Advanced Projects**
        - Complete 1-2 advanced projects
        - Contribute to open source projects
        - Prepare for technical interviews
        
        **Key Success Factors:**
        
        1. **Consistency**: Work on projects regularly, even if just 1-2 hours per day
        2. **Documentation**: Write clear README files and document your learning process
        3. **Code Quality**: Follow best practices and write clean, maintainable code
        4. **Version Control**: Use Git effectively and commit frequently
        5. **Networking**: Share your projects on LinkedIn and GitHub
        6. **Feedback**: Get feedback from peers and professionals
        
        **Portfolio Website Checklist:**
        - [ ] Professional headshot and bio
        - [ ] Project showcase with live demos
        - [ ] Skills section with proficiency levels
        - [ ] Contact information and resume
        - [ ] Blog section for technical articles
        - [ ] Mobile-responsive design
        
        **GitHub Profile Optimization:**
        - [ ] Professional profile picture
        - [ ] Compelling bio and location
        - [ ] Pinned repositories (top 6 projects)
        - [ ] Consistent commit history
        - [ ] Well-documented README files
        - [ ] Active contribution to open source
        
        **Next Steps:**
        1. Choose your first project from the recommendations above
        2. Set up your development environment
        3. Create a project timeline and milestones
        4. Start coding and documenting your progress
        5. Share your journey on social media and professional networks
        """
        
        return plan
