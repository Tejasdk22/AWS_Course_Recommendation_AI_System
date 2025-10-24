"""
AWS Lambda function for ResumeAnalysisAgent
Analyzes user resumes and provides personalized recommendations
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime
import re
import PyPDF2
import docx
from io import BytesIO

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for ResumeAnalysisAgent
    Analyzes uploaded resumes and provides personalized recommendations
    """
    
    try:
        # Extract resume data from event
        resume_data = event.get('resume_data', '')
        resume_text = event.get('resume_text', '')
        career_goal = event.get('career_goal', 'data scientist')
        major = event.get('major', 'Business Analytics')
        session_id = event.get('sessionId', '')
        
        print(f"ResumeAnalysisAgent processing resume for: {career_goal}")
        
        # Initialize agent
        agent = ResumeAnalysisAgent()
        
        # Analyze resume
        analysis_result = agent.analyze_resume(resume_text, career_goal, major)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'ResumeAnalysisAgent',
                'career_goal': career_goal,
                'major': major,
                'analysis': analysis_result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in ResumeAnalysisAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'ResumeAnalysisAgent'
            }
        }

class ResumeAnalysisAgent:
    """Resume Analysis Agent that analyzes user resumes and provides personalized recommendations"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'utd-career-guidance-resumes'
        
    def analyze_resume(self, resume_text: str, career_goal: str, major: str) -> Dict[str, Any]:
        """Analyze resume and provide personalized recommendations"""
        
        # Extract skills from resume
        current_skills = self._extract_skills_from_resume(resume_text)
        
        # Extract experience from resume
        experience = self._extract_experience_from_resume(resume_text)
        
        # Extract education from resume
        education = self._extract_education_from_resume(resume_text)
        
        # Identify skill gaps
        skill_gaps = self._identify_skill_gaps(current_skills, career_goal)
        
        # Generate personalized recommendations
        recommendations = self._generate_personalized_recommendations(
            current_skills, skill_gaps, experience, education, career_goal, major
        )
        
        # Generate resume optimization suggestions
        optimization_suggestions = self._generate_resume_optimization_suggestions(
            current_skills, skill_gaps, career_goal
        )
        
        return {
            'current_skills': current_skills,
            'experience': experience,
            'education': education,
            'skill_gaps': skill_gaps,
            'personalized_recommendations': recommendations,
            'resume_optimization': optimization_suggestions,
            'career_readiness_score': self._calculate_career_readiness_score(current_skills, career_goal),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _extract_skills_from_resume(self, resume_text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        text_lower = resume_text.lower()
        
        # Technical skills
        technical_skills = {
            'Python': ['python', 'pandas', 'numpy', 'scikit-learn', 'django', 'flask'],
            'R': ['r', 'rstudio', 'shiny', 'tidyverse'],
            'SQL': ['sql', 'mysql', 'postgresql', 'sqlite', 'oracle'],
            'JavaScript': ['javascript', 'js', 'node.js', 'react', 'angular', 'vue'],
            'Java': ['java', 'spring', 'hibernate', 'maven'],
            'Machine Learning': ['machine learning', 'ml', 'tensorflow', 'pytorch', 'scikit-learn'],
            'Data Analysis': ['data analysis', 'statistics', 'regression', 'classification'],
            'Cloud Computing': ['aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes'],
            'Database': ['database', 'mongodb', 'redis', 'cassandra'],
            'Web Development': ['html', 'css', 'bootstrap', 'jquery', 'django', 'flask'],
            'Data Visualization': ['tableau', 'power bi', 'matplotlib', 'seaborn', 'plotly'],
            'Big Data': ['hadoop', 'spark', 'kafka', 'hive', 'pig'],
            'Statistics': ['statistics', 'statistical', 'hypothesis testing', 'a/b testing'],
            'Business Intelligence': ['business intelligence', 'bi', 'etl', 'data warehousing']
        }
        
        for skill, keywords in technical_skills.items():
            if any(keyword in text_lower for keyword in keywords):
                skills.append(skill)
        
        # Soft skills
        soft_skills = {
            'Leadership': ['leadership', 'lead', 'managed', 'supervised', 'directed'],
            'Communication': ['communication', 'presented', 'presentation', 'spoke'],
            'Problem Solving': ['problem solving', 'solved', 'resolved', 'troubleshoot'],
            'Teamwork': ['teamwork', 'collaborated', 'team', 'group'],
            'Project Management': ['project management', 'managed projects', 'project lead']
        }
        
        for skill, keywords in soft_skills.items():
            if any(keyword in text_lower for keyword in keywords):
                skills.append(skill)
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_experience_from_resume(self, resume_text: str) -> List[Dict[str, Any]]:
        """Extract work experience from resume"""
        experience = []
        
        # Look for experience patterns
        experience_patterns = [
            r'(\d{4})\s*-\s*(\d{4}|\w+)\s*([^\\n]+)',
            r'(\d{4})\s*-\s*Present\s*([^\\n]+)',
            r'(\d{4})\s*-\s*Current\s*([^\\n]+)'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    experience.append({
                        'duration': f"{match[0]} - {match[1] if len(match) > 1 else 'Present'}",
                        'position': match[2] if len(match) > 2 else 'Unknown',
                        'company': 'Unknown'
                    })
        
        return experience[:5]  # Limit to 5 most recent experiences
    
    def _extract_education_from_resume(self, resume_text: str) -> List[Dict[str, Any]]:
        """Extract education from resume"""
        education = []
        
        # Look for education patterns
        education_patterns = [
            r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|Ph\.D\.)\s+[^\\n]+',
            r'(University|College|Institute)\s+[^\\n]+',
            r'(GPA|Grade Point Average)\s*:?\s*(\d+\.?\d*)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'degree': match[0] if isinstance(match, tuple) else match,
                    'institution': 'Unknown',
                    'gpa': 'Not specified'
                })
        
        return education[:3]  # Limit to 3 most recent degrees
    
    def _identify_skill_gaps(self, current_skills: List[str], career_goal: str) -> List[str]:
        """Identify skill gaps for career goal"""
        
        # Define required skills for different career goals
        career_skill_requirements = {
            'data scientist': [
                'Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis',
                'Data Visualization', 'R', 'Pandas', 'NumPy', 'Scikit-learn'
            ],
            'data analyst': [
                'SQL', 'Excel', 'Tableau', 'Power BI', 'Statistics', 'Data Analysis',
                'Python', 'R', 'Data Visualization'
            ],
            'data engineer': [
                'Python', 'SQL', 'Big Data', 'Cloud Computing', 'Database',
                'ETL', 'Hadoop', 'Spark', 'AWS', 'Docker'
            ],
            'software engineer': [
                'Programming', 'Java', 'Python', 'JavaScript', 'Database',
                'Web Development', 'Cloud Computing', 'Git', 'Docker'
            ],
            'business analyst': [
                'Business Intelligence', 'SQL', 'Excel', 'Statistics',
                'Communication', 'Problem Solving', 'Project Management'
            ]
        }
        
        required_skills = career_skill_requirements.get(career_goal.lower(), [])
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        skill_gaps = []
        for required_skill in required_skills:
            if required_skill.lower() not in current_skills_lower:
                skill_gaps.append(required_skill)
        
        return skill_gaps[:10]  # Limit to top 10 skill gaps
    
    def _generate_personalized_recommendations(self, current_skills: List[str], skill_gaps: List[str], 
                                            experience: List[Dict], education: List[Dict], 
                                            career_goal: str, major: str) -> Dict[str, Any]:
        """Generate personalized recommendations based on resume analysis"""
        
        recommendations = {
            'strengths': current_skills[:5],  # Top 5 strengths
            'skill_gaps': skill_gaps[:5],     # Top 5 skill gaps
            'experience_level': self._assess_experience_level(experience),
            'education_level': self._assess_education_level(education),
            'personalized_courses': self._recommend_personalized_courses(skill_gaps, major),
            'personalized_projects': self._recommend_personalized_projects(skill_gaps, career_goal),
            'career_timeline': self._generate_career_timeline(current_skills, skill_gaps, career_goal)
        }
        
        return recommendations
    
    def _assess_experience_level(self, experience: List[Dict]) -> str:
        """Assess experience level based on work history"""
        if len(experience) == 0:
            return 'Entry Level (0-1 years)'
        elif len(experience) <= 2:
            return 'Junior Level (1-3 years)'
        elif len(experience) <= 4:
            return 'Mid Level (3-5 years)'
        else:
            return 'Senior Level (5+ years)'
    
    def _assess_education_level(self, education: List[Dict]) -> str:
        """Assess education level"""
        if not education:
            return 'High School'
        
        degrees = [edu.get('degree', '').lower() for edu in education]
        if any('phd' in degree or 'ph.d' in degree for degree in degrees):
            return 'PhD'
        elif any('master' in degree or 'm.s' in degree for degree in degrees):
            return 'Master\'s'
        elif any('bachelor' in degree or 'b.s' in degree for degree in degrees):
            return 'Bachelor\'s'
        else:
            return 'Associate\'s or Certificate'
    
    def _recommend_personalized_courses(self, skill_gaps: List[str], major: str) -> List[str]:
        """Recommend personalized courses based on skill gaps and major"""
        
        course_recommendations = []
        
        # Map skill gaps to UTD courses
        skill_to_course_mapping = {
            'Python': ['CS 1336 - Computer Science I', 'CS 2336 - Computer Science II'],
            'Machine Learning': ['CS 6375 - Machine Learning', 'BUAN 4342 - Data Mining and Machine Learning'],
            'Statistics': ['STAT 3331 - Probability and Statistics', 'MATH 3330 - Probability and Statistics'],
            'SQL': ['MIS 4356 - Database Systems', 'CS 4352 - Database Systems'],
            'Data Visualization': ['MIS 4354 - Data Visualization', 'BUAN 4344 - Business Intelligence'],
            'Business Intelligence': ['BUAN 4344 - Business Intelligence', 'BUAN 4345 - Business Intelligence and Analytics']
        }
        
        for skill_gap in skill_gaps[:5]:  # Focus on top 5 skill gaps
            if skill_gap in skill_to_course_mapping:
                course_recommendations.extend(skill_to_course_mapping[skill_gap])
        
        return list(set(course_recommendations))[:8]  # Remove duplicates and limit to 8 courses
    
    def _recommend_personalized_projects(self, skill_gaps: List[str], career_goal: str) -> List[str]:
        """Recommend personalized projects based on skill gaps and career goal"""
        
        project_recommendations = []
        
        # Map skill gaps to project types
        skill_to_project_mapping = {
            'Python': ['Build a Python web scraper', 'Create a data analysis dashboard'],
            'Machine Learning': ['Implement a recommendation system', 'Build a classification model'],
            'Statistics': ['Conduct A/B testing analysis', 'Perform statistical hypothesis testing'],
            'SQL': ['Design and implement a database', 'Create complex SQL queries'],
            'Data Visualization': ['Create interactive dashboards', 'Build data visualization tools']
        }
        
        for skill_gap in skill_gaps[:5]:
            if skill_gap in skill_to_project_mapping:
                project_recommendations.extend(skill_to_project_mapping[skill_gap])
        
        return list(set(project_recommendations))[:5]  # Remove duplicates and limit to 5 projects
    
    def _generate_career_timeline(self, current_skills: List[str], skill_gaps: List[str], career_goal: str) -> Dict[str, str]:
        """Generate career development timeline"""
        
        timeline = {
            'immediate (0-3 months)': f'Focus on developing {skill_gaps[0] if skill_gaps else "Python"} skills',
            'short-term (3-6 months)': f'Complete 2-3 courses related to {career_goal}',
            'medium-term (6-12 months)': f'Build portfolio projects showcasing {career_goal} skills',
            'long-term (1-2 years)': f'Apply for {career_goal} positions with strong portfolio'
        }
        
        return timeline
    
    def _generate_resume_optimization_suggestions(self, current_skills: List[str], skill_gaps: List[str], career_goal: str) -> List[str]:
        """Generate resume optimization suggestions"""
        
        suggestions = []
        
        # Skills section suggestions
        if len(current_skills) < 10:
            suggestions.append('Add more technical skills to your resume')
        
        # Skill gaps suggestions
        if skill_gaps:
            suggestions.append(f'Consider highlighting experience with: {", ".join(skill_gaps[:3])}')
        
        # Career goal alignment
        suggestions.append(f'Emphasize experiences relevant to {career_goal} roles')
        
        # General suggestions
        suggestions.extend([
            'Use action verbs to describe your achievements',
            'Quantify your accomplishments with numbers and metrics',
            'Include relevant keywords from job descriptions',
            'Keep your resume to 1-2 pages maximum'
        ])
        
        return suggestions[:6]  # Limit to 6 suggestions
    
    def _calculate_career_readiness_score(self, current_skills: List[str], career_goal: str) -> int:
        """Calculate career readiness score (0-100)"""
        
        # Define required skills for career goal
        career_skill_requirements = {
            'data scientist': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis'],
            'data analyst': ['SQL', 'Excel', 'Statistics', 'Data Analysis', 'Python'],
            'data engineer': ['Python', 'SQL', 'Big Data', 'Cloud Computing', 'Database'],
            'software engineer': ['Programming', 'Java', 'Python', 'JavaScript', 'Database'],
            'business analyst': ['Business Intelligence', 'SQL', 'Excel', 'Statistics', 'Communication']
        }
        
        required_skills = career_skill_requirements.get(career_goal.lower(), [])
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        if not required_skills:
            return 50  # Default score if career goal not found
        
        # Calculate percentage of required skills possessed
        possessed_skills = sum(1 for skill in required_skills if skill.lower() in current_skills_lower)
        readiness_score = int((possessed_skills / len(required_skills)) * 100)
        
        return min(readiness_score, 100)  # Cap at 100

if __name__ == "__main__":
    # Test the agent
    test_event = {
        'resume_text': 'I have experience with Python, SQL, and data analysis. I worked as a data analyst for 2 years.',
        'career_goal': 'data scientist',
        'major': 'Business Analytics',
        'sessionId': 'test123'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
