"""
AWS Lambda function for CareerMatchingAgent in Bedrock AgentCore
Autonomous career matching and recommendation agent
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime
import requests

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for CareerMatchingAgent
    Processes career matching requests autonomously
    """
    
    try:
        # Extract query from event
        query = event.get('query', '')
        session_id = event.get('sessionId', '')
        
        print(f"CareerMatchingAgent processing query: {query}")
        
        # Initialize agent
        agent = CareerMatchingAgent()
        
        # Process the query autonomously
        result = agent.process_career_matching_query(query)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'CareerMatchingAgent',
                'query': query,
                'result': result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in CareerMatchingAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'CareerMatchingAgent'
            }
        }

class CareerMatchingAgent:
    """Autonomous Career Matching Agent"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'utd-career-guidance-data'
        self.lambda_client = boto3.client('lambda')
        
    def process_career_matching_query(self, query: str) -> Dict[str, Any]:
        """Process career matching query autonomously"""
        
        # Extract career goals from query
        career_goals = self._extract_career_goals(query)
        
        # Get job market data from JobMarketAgent
        job_market_data = self._get_job_market_data(career_goals)
        
        # Get course catalog data from CourseCatalogAgent
        course_catalog_data = self._get_course_catalog_data(career_goals)
        
        # Perform career matching analysis
        matching_analysis = self._analyze_career_matching(job_market_data, course_catalog_data, career_goals)
        
        # Generate personalized recommendations
        recommendations = self._generate_career_recommendations(matching_analysis, query)
        
        return {
            'career_goals': career_goals,
            'job_market_data': job_market_data,
            'course_catalog_data': course_catalog_data,
            'matching_analysis': matching_analysis,
            'recommendations': recommendations,
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
    
    def _get_job_market_data(self, career_goals: List[str]) -> Dict[str, Any]:
        """Get job market data from JobMarketAgent"""
        try:
            # Invoke JobMarketAgent Lambda function
            response = self.lambda_client.invoke(
                FunctionName='utd-career-guidance-job_market_agent',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': ' '.join(career_goals),
                    'sessionId': f"career-matching-{datetime.now().timestamp()}"
                })
            )
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                return result['body']['result']
            else:
                return {'error': 'Failed to get job market data'}
                
        except Exception as e:
            print(f"Error getting job market data: {e}")
            return {'error': str(e)}
    
    def _get_course_catalog_data(self, career_goals: List[str]) -> Dict[str, Any]:
        """Get course catalog data from CourseCatalogAgent"""
        try:
            # Invoke CourseCatalogAgent Lambda function
            response = self.lambda_client.invoke(
                FunctionName='utd-career-guidance-course_catalog_agent',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': ' '.join(career_goals),
                    'sessionId': f"career-matching-{datetime.now().timestamp()}"
                })
            )
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                return result['body']['result']
            else:
                return {'error': 'Failed to get course catalog data'}
                
        except Exception as e:
            print(f"Error getting course catalog data: {e}")
            return {'error': str(e)}
    
    def _analyze_career_matching(self, job_market_data: Dict[str, Any], 
                                course_catalog_data: Dict[str, Any], 
                                career_goals: List[str]) -> Dict[str, Any]:
        """Analyze career matching between job market and course offerings"""
        
        if 'error' in job_market_data or 'error' in course_catalog_data:
            return {'error': 'Unable to analyze career matching due to data errors'}
        
        # Extract skills from job market data
        job_skills = []
        if 'analysis' in job_market_data and 'top_skills' in job_market_data['analysis']:
            job_skills = [skill for skill, count in job_market_data['analysis']['top_skills']]
        
        # Extract skills from course catalog data
        course_skills = []
        if 'analysis' in course_catalog_data and 'top_skills' in course_catalog_data['analysis']:
            course_skills = [skill for skill, count in course_catalog_data['analysis']['top_skills']]
        
        # Find skill matches and gaps
        skill_matches = list(set(job_skills) & set(course_skills))
        skill_gaps = list(set(job_skills) - set(course_skills))
        additional_skills = list(set(course_skills) - set(job_skills))
        
        # Calculate matching score
        total_job_skills = len(job_skills)
        matched_skills = len(skill_matches)
        matching_score = (matched_skills / total_job_skills * 100) if total_job_skills > 0 else 0
        
        return {
            'job_skills': job_skills,
            'course_skills': course_skills,
            'skill_matches': skill_matches,
            'skill_gaps': skill_gaps,
            'additional_skills': additional_skills,
            'matching_score': matching_score,
            'total_job_skills': total_job_skills,
            'matched_skills': matched_skills
        }
    
    def _generate_career_recommendations(self, matching_analysis: Dict[str, Any], query: str) -> str:
        """Generate personalized career recommendations"""
        
        if 'error' in matching_analysis:
            return f"Unable to generate recommendations: {matching_analysis['error']}"
        
        recommendations = f"""
        **Career Matching Analysis for: {query}**
        
        **Matching Overview:**
        - Job market skills analyzed: {matching_analysis['total_job_skills']}
        - Skills matched with courses: {matching_analysis['matched_skills']}
        - Matching score: {matching_analysis['matching_score']:.1f}%
        
        **Matched Skills (Available in UTD Courses):**
        """
        
        for i, skill in enumerate(matching_analysis['skill_matches'][:8], 1):
            recommendations += f"{i}. {skill}\n"
        
        if matching_analysis['skill_gaps']:
            recommendations += f"""
        
        **Skill Gaps (Not Covered in UTD Courses):**
        """
            for i, skill in enumerate(matching_analysis['skill_gaps'][:5], 1):
                recommendations += f"{i}. {skill}\n"
        
        if matching_analysis['additional_skills']:
            recommendations += f"""
        
        **Additional Skills (Available in UTD but Not in High Demand):**
        """
            for i, skill in enumerate(matching_analysis['additional_skills'][:5], 1):
                recommendations += f"{i}. {skill}\n"
        
        recommendations += f"""
        
        **Career Path Recommendations:**
        
        1. **Immediate Actions:**
           - Focus on courses that cover the matched skills
           - Prioritize the top 3 matched skills for your career goals
           - Consider taking additional courses to fill skill gaps
        
        2. **Course Selection Strategy:**
           - Start with courses covering matched skills
           - Look for courses that teach multiple matched skills
           - Consider prerequisites and course sequences
        
        3. **Skill Development Plan:**
           - Develop matched skills through coursework
           - Address skill gaps through self-study or external courses
           - Build a portfolio showcasing your skills
        
        4. **Career Progression:**
           - Target roles that require the matched skills
           - Consider internships or projects in your target field
           - Network with professionals in your desired career path
        
        **Next Steps:**
        - Review specific UTD courses that cover matched skills
        - Create a study plan for skill gap areas
        - Consider practical projects to demonstrate your skills
        - Connect with career services for additional guidance
        """
        
        return recommendations
