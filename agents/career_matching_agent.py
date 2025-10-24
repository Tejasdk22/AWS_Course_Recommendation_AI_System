"""
Course Recommendation Matching Agent for AWS Course Recommendation AI System
Matches job market requirements with course offerings using cosine similarity
"""

import json
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import re
from datetime import datetime
try:
    from .base_agent import BaseAgent
except ImportError:
    from base_agent import BaseAgent


class CareerMatchingAgent(BaseAgent):
    """
    Agent responsible for matching job market requirements with course offerings
    and providing career guidance recommendations.
    """
    
    def __init__(self):
        super().__init__("CareerMatchingAgent")
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,  # Changed from 2 to 1 to avoid empty vocabulary
            max_df=0.95
        )
        self.scaler = StandardScaler()
        self.job_market_data = None
        self.course_catalog_data = None
    
    async def fetch_data(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Fetch job market and course catalog data for matching.
        
        Returns:
            Tuple of (job_market_data, course_catalog_data)
        """
        self.logger.info("Fetching data for career matching")
        
        # Load job market data
        job_market_data = self.load_data('job_market_analysis.json')
        if not job_market_data:
            self.logger.warning("No job market data found, using sample data")
            job_market_data = self._create_sample_job_data()
        
        # Load course catalog data
        course_catalog_data = self.load_data('course_catalog_analysis.json')
        if not course_catalog_data:
            self.logger.warning("No course catalog data found, using sample data")
            course_catalog_data = self._create_sample_course_data()
        
        self.job_market_data = job_market_data
        self.course_catalog_data = course_catalog_data
        
        return job_market_data, course_catalog_data
    
    def _create_sample_job_data(self) -> Dict[str, Any]:
        """Create sample job market data for testing."""
        return {
            'total_jobs': 50,
            'skills_analysis': {
                'top_skills': [
                    ('Python', 35), ('Machine Learning', 28), ('SQL', 25),
                    ('Data Analysis', 22), ('Statistics', 20), ('AWS', 18),
                    ('TensorFlow', 15), ('Pandas', 14), ('R', 12),
                    ('Tableau', 10), ('Deep Learning', 9), ('Scikit-learn', 8)
                ],
                'total_unique_skills': 45,
                'skills_frequency': {
                    'Python': 35, 'Machine Learning': 28, 'SQL': 25,
                    'Data Analysis': 22, 'Statistics': 20, 'AWS': 18
                }
            },
            'salary_analysis': {
                'average_salary': 95000,
                'min_salary': 65000,
                'max_salary': 140000,
                'salary_count': 30
            },
            'raw_jobs': [
                {
                    'title': 'Senior Data Scientist',
                    'company': 'Tech Corp',
                    'skills': ['Python', 'Machine Learning', 'SQL', 'AWS'],
                    'salary': '120000-140000'
                }
            ]
        }
    
    def _create_sample_course_data(self) -> Dict[str, Any]:
        """Create sample course catalog data for testing."""
        return {
            'total_courses': 30,
            'skills_analysis': {
                'top_skills': [
                    ('Python', 15), ('Machine Learning', 12), ('Statistics', 10),
                    ('Data Analysis', 8), ('SQL', 7), ('Linear Algebra', 6),
                    ('Calculus', 5), ('R', 4), ('AWS', 3)
                ]
            },
            'course_skills_mapping': {
                'CS 4375': {
                    'title': 'Machine Learning',
                    'skills': ['Python', 'Machine Learning', 'Statistics', 'Scikit-learn'],
                    'department': 'CS',
                    'level': 'undergraduate'
                },
                'CS 6313': {
                    'title': 'Statistical Methods for Data Science',
                    'skills': ['Statistics', 'R', 'Data Analysis', 'Linear Algebra'],
                    'department': 'CS',
                    'level': 'graduate'
                }
            }
        }
    
    def process_data(self, data: Tuple[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process job market and course data to create career matching analysis.
        
        Args:
            data: Tuple of (job_market_data, course_catalog_data)
            
        Returns:
            Processed career matching analysis
        """
        job_market_data, course_catalog_data = data
        
        self.logger.info("Processing career matching data")
        
        # Extract job skills and course skills
        job_skills = self._extract_job_skills(job_market_data)
        course_skills = self._extract_course_skills(course_catalog_data)
        
        # Create skill vectors
        job_vectors, course_vectors, skill_vocabulary = self._create_skill_vectors(
            job_skills, course_skills
        )
        
        # Calculate similarity matrix
        similarity_matrix = self._calculate_similarity_matrix(job_vectors, course_vectors)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            job_skills, course_skills, similarity_matrix, skill_vocabulary
        )
        
        # Analyze skill gaps
        skill_gaps = self._analyze_skill_gaps(job_skills, course_skills)
        
        # Create career paths
        career_paths = self._create_career_paths(
            job_market_data, course_catalog_data, recommendations
        )
        
        processed_data = {
            'job_skills_analysis': {
                'total_job_skills': len(job_skills),
                'top_job_skills': self._get_top_skills(job_skills, 20),
                'skill_frequency': job_skills
            },
            'course_skills_analysis': {
                'total_course_skills': len(course_skills),
                'top_course_skills': self._get_top_skills(course_skills, 20),
                'skill_frequency': course_skills
            },
            'similarity_analysis': {
                'average_similarity': float(np.mean(similarity_matrix)),
                'max_similarity': float(np.max(similarity_matrix)),
                'min_similarity': float(np.min(similarity_matrix))
            },
            'recommendations': recommendations,
            'skill_gaps': skill_gaps,
            'career_paths': career_paths,
            'skill_vocabulary': skill_vocabulary,
            'processed_at': datetime.now().isoformat()
        }
        
        self.logger.info("Career matching data processing completed")
        return processed_data
    
    def _extract_job_skills(self, job_market_data: Dict[str, Any]) -> Dict[str, int]:
        """Extract and count skills from job market data."""
        skills_freq = {}
        
        # Get skills from skills_analysis
        if 'skills_analysis' in job_market_data:
            skills_freq.update(job_market_data['skills_analysis'].get('skills_frequency', {}))
        
        # Also extract from raw jobs
        if 'raw_jobs' in job_market_data:
            for job in job_market_data['raw_jobs']:
                job_skills = job.get('skills', [])
                for skill in job_skills:
                    skills_freq[skill] = skills_freq.get(skill, 0) + 1
        
        return skills_freq
    
    def _extract_course_skills(self, course_catalog_data: Dict[str, Any]) -> Dict[str, int]:
        """Extract and count skills from course catalog data."""
        skills_freq = {}
        
        # Get skills from skills_analysis
        if 'skills_analysis' in course_catalog_data:
            skills_freq.update(course_catalog_data['skills_analysis'].get('skills_frequency', {}))
        
        # Also extract from course_skills_mapping
        if 'course_skills_mapping' in course_catalog_data:
            for course_code, course_info in course_catalog_data['course_skills_mapping'].items():
                course_skills = course_info.get('skills', [])
                for skill in course_skills:
                    skills_freq[skill] = skills_freq.get(skill, 0) + 1
        
        return skills_freq
    
    def _create_skill_vectors(self, job_skills: Dict[str, int], 
                            course_skills: Dict[str, int]) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Create TF-IDF vectors for job and course skills."""
        # Combine all skills
        all_skills = set(job_skills.keys()) | set(course_skills.keys())
        skill_vocabulary = sorted(list(all_skills))
        
        # Create documents for vectorization
        job_doc = ' '.join([skill for skill, freq in job_skills.items() for _ in range(freq)])
        course_doc = ' '.join([skill for skill, freq in course_skills.items() for _ in range(freq)])
        
        # Vectorize
        documents = [job_doc, course_doc]
        vectors = self.vectorizer.fit_transform(documents).toarray()
        
        job_vector = vectors[0].reshape(1, -1)
        course_vector = vectors[1].reshape(1, -1)
        
        return job_vector, course_vector, skill_vocabulary
    
    def _calculate_similarity_matrix(self, job_vectors: np.ndarray, 
                                   course_vectors: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between job and course vectors."""
        return cosine_similarity(job_vectors, course_vectors)
    
    def _generate_recommendations(self, job_skills: Dict[str, int], 
                                course_skills: Dict[str, int],
                                similarity_matrix: np.ndarray,
                                skill_vocabulary: List[str]) -> List[Dict[str, Any]]:
        """Generate career recommendations based on skill matching."""
        recommendations = []
        
        # Find skills that are in high demand but low supply
        skill_demand_supply = {}
        for skill in skill_vocabulary:
            demand = job_skills.get(skill, 0)
            supply = course_skills.get(skill, 0)
            if demand > 0 or supply > 0:
                skill_demand_supply[skill] = {
                    'demand': demand,
                    'supply': supply,
                    'gap': demand - supply,
                    'ratio': demand / max(supply, 1)
                }
        
        # Sort by gap (high demand, low supply)
        sorted_skills = sorted(
            skill_demand_supply.items(),
            key=lambda x: x[1]['gap'],
            reverse=True
        )
        
        # Create recommendations
        for skill, metrics in sorted_skills[:10]:
            if metrics['gap'] > 0:  # Skills in high demand
                recommendations.append({
                    'skill': skill,
                    'demand_score': metrics['demand'],
                    'supply_score': metrics['supply'],
                    'gap_score': metrics['gap'],
                    'recommendation': 'High Priority - Focus on learning this skill',
                    'priority': 'High'
                })
            elif metrics['ratio'] > 2:  # Skills with high demand/supply ratio
                recommendations.append({
                    'skill': skill,
                    'demand_score': metrics['demand'],
                    'supply_score': metrics['supply'],
                    'gap_score': metrics['gap'],
                    'recommendation': 'Medium Priority - Consider learning this skill',
                    'priority': 'Medium'
                })
        
        return recommendations
    
    def _analyze_skill_gaps(self, job_skills: Dict[str, int], 
                          course_skills: Dict[str, int]) -> Dict[str, Any]:
        """Analyze skill gaps between job market and course offerings."""
        all_skills = set(job_skills.keys()) | set(course_skills.keys())
        
        gaps = {
            'high_demand_low_supply': [],
            'high_supply_low_demand': [],
            'missing_from_courses': [],
            'missing_from_jobs': []
        }
        
        for skill in all_skills:
            job_freq = job_skills.get(skill, 0)
            course_freq = course_skills.get(skill, 0)
            
            if job_freq > 5 and course_freq < 3:  # High demand, low supply
                gaps['high_demand_low_supply'].append({
                    'skill': skill,
                    'job_frequency': job_freq,
                    'course_frequency': course_freq
                })
            elif course_freq > 5 and job_freq < 3:  # High supply, low demand
                gaps['high_supply_low_demand'].append({
                    'skill': skill,
                    'job_frequency': job_freq,
                    'course_frequency': course_freq
                })
            elif job_freq > 0 and course_freq == 0:  # Missing from courses
                gaps['missing_from_courses'].append({
                    'skill': skill,
                    'job_frequency': job_freq
                })
            elif course_freq > 0 and job_freq == 0:  # Missing from jobs
                gaps['missing_from_jobs'].append({
                    'skill': skill,
                    'course_frequency': course_freq
                })
        
        return gaps
    
    def _create_career_paths(self, job_market_data: Dict[str, Any],
                           course_catalog_data: Dict[str, Any],
                           recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create career paths based on job market and course data."""
        career_paths = []
        
        # Data Scientist path
        data_scientist_skills = ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Analysis']
        data_scientist_courses = self._find_courses_for_skills(
            course_catalog_data, data_scientist_skills
        )
        
        career_paths.append({
            'career_title': 'Data Scientist',
            'required_skills': data_scientist_skills,
            'recommended_courses': data_scientist_courses,
            'salary_range': job_market_data.get('salary_analysis', {}).get('average_salary', 0),
            'difficulty': 'Intermediate',
            'time_to_complete': '6-12 months'
        })
        
        # Machine Learning Engineer path
        ml_engineer_skills = ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'AWS']
        ml_engineer_courses = self._find_courses_for_skills(
            course_catalog_data, ml_engineer_skills
        )
        
        career_paths.append({
            'career_title': 'Machine Learning Engineer',
            'required_skills': ml_engineer_skills,
            'recommended_courses': ml_engineer_courses,
            'salary_range': job_market_data.get('salary_analysis', {}).get('average_salary', 0) + 10000,
            'difficulty': 'Advanced',
            'time_to_complete': '9-15 months'
        })
        
        # Data Analyst path
        data_analyst_skills = ['SQL', 'Python', 'Data Analysis', 'Tableau', 'Statistics']
        data_analyst_courses = self._find_courses_for_skills(
            course_catalog_data, data_analyst_skills
        )
        
        career_paths.append({
            'career_title': 'Data Analyst',
            'required_skills': data_analyst_skills,
            'recommended_courses': data_analyst_courses,
            'salary_range': job_market_data.get('salary_analysis', {}).get('average_salary', 0) - 15000,
            'difficulty': 'Beginner',
            'time_to_complete': '3-6 months'
        })
        
        return career_paths
    
    def _find_courses_for_skills(self, course_catalog_data: Dict[str, Any], 
                               target_skills: List[str]) -> List[Dict[str, Any]]:
        """Find courses that cover the target skills."""
        courses = []
        
        if 'course_skills_mapping' not in course_catalog_data:
            return courses
        
        for course_code, course_info in course_catalog_data['course_skills_mapping'].items():
            course_skills = course_info.get('skills', [])
            skill_overlap = set(target_skills) & set(course_skills)
            
            if skill_overlap:
                courses.append({
                    'course_code': course_code,
                    'course_title': course_info.get('title', ''),
                    'matching_skills': list(skill_overlap),
                    'skill_coverage': len(skill_overlap) / len(target_skills),
                    'department': course_info.get('department', ''),
                    'level': course_info.get('level', '')
                })
        
        # Sort by skill coverage
        courses.sort(key=lambda x: x['skill_coverage'], reverse=True)
        return courses[:5]  # Return top 5 courses
    
    def _get_top_skills(self, skills_freq: Dict[str, int], limit: int = 20) -> List[tuple]:
        """Get top skills by frequency."""
        return sorted(skills_freq.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    async def respond(self, processed_data: Dict[str, Any], user_query: str = None) -> str:
        """
        Generate a response based on processed career matching data.
        
        Args:
            processed_data: Processed career matching analysis
            user_query: Optional user query for context
            
        Returns:
            Generated response about career matching and recommendations
        """
        if not processed_data:
            return "No career matching data available to analyze."
        
        # Save processed data
        self.save_data(processed_data, 'career_matching_analysis.json')
        
        # Generate response using Bedrock
        prompt = self._create_career_matching_prompt(processed_data, user_query)
        response = await self.invoke_bedrock(prompt)
        
        return response
    
    def _create_career_matching_prompt(self, data: Dict[str, Any], user_query: str = None) -> str:
        """Create a prompt for career matching analysis."""
        
        recommendations = data.get('recommendations', [])
        skill_gaps = data.get('skill_gaps', {})
        career_paths = data.get('career_paths', [])
        
        prompt = f"""
        As a career guidance AI, analyze the following career matching data:

        **Career Matching Overview:**
        - Analysis date: {data.get('processed_at', 'N/A')}
        - Similarity score: {data.get('similarity_analysis', {}).get('average_similarity', 0):.3f}

        **Top Skill Recommendations:**
        {self._format_recommendations_list(recommendations[:10])}

        **Skill Gap Analysis:**
        - High demand, low supply skills: {len(skill_gaps.get('high_demand_low_supply', []))}
        - Missing from courses: {len(skill_gaps.get('missing_from_courses', []))}
        - Missing from jobs: {len(skill_gaps.get('missing_from_jobs', []))}

        **Available Career Paths:**
        {self._format_career_paths_list(career_paths)}

        **User Query:** {user_query or 'General career matching analysis'}

        Please provide:
        1. Analysis of skill demand vs supply in the market
        2. Top priority skills to learn based on market demand
        3. Recommended career paths with specific course recommendations
        4. Skill gaps that need attention
        5. Actionable steps for career development

        Format your response in a clear, actionable manner suitable for career guidance.
        """
        
        return prompt
    
    def _format_recommendations_list(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format recommendations list for display."""
        if not recommendations:
            return "No recommendations available"
        
        formatted = []
        for i, rec in enumerate(recommendations, 1):
            formatted.append(
                f"{i}. {rec['skill']} - {rec['recommendation']} "
                f"(Demand: {rec['demand_score']}, Supply: {rec['supply_score']})"
            )
        
        return "\n".join(formatted)
    
    def _format_career_paths_list(self, career_paths: List[Dict[str, Any]]) -> str:
        """Format career paths list for display."""
        if not career_paths:
            return "No career paths available"
        
        formatted = []
        for i, path in enumerate(career_paths, 1):
            formatted.append(
                f"{i}. {path['career_title']} - ${path['salary_range']:,.0f} "
                f"({path['difficulty']}, {path['time_to_complete']})"
            )
        
        return "\n".join(formatted)
