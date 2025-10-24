"""
AWS Lambda function for JobMarketAgent in Bedrock AgentCore
Autonomous job market analysis agent
"""

import json
import boto3
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import asyncio
import aiohttp
from datetime import datetime

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for JobMarketAgent
    Processes job market analysis requests autonomously
    """
    
    try:
        # Extract query from event
        query = event.get('query', '')
        session_id = event.get('sessionId', '')
        
        print(f"JobMarketAgent processing query: {query}")
        
        # Initialize agent
        agent = JobMarketAgent()
        
        # Process the query autonomously
        result = agent.process_job_market_query(query)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'JobMarketAgent',
                'query': query,
                'result': result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in JobMarketAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'JobMarketAgent'
            }
        }

class JobMarketAgent:
    """Autonomous Job Market Analysis Agent"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'utd-career-guidance-data'
        
    def process_job_market_query(self, query: str) -> Dict[str, Any]:
        """Process job market query autonomously"""
        
        # Extract career keywords from query
        career_keywords = self._extract_career_keywords(query)
        
        # Scrape job postings autonomously
        job_data = self._scrape_job_postings(career_keywords)
        
        # Analyze market trends
        analysis = self._analyze_market_trends(job_data)
        
        # Generate insights
        insights = self._generate_insights(analysis, query)
        
        return {
            'career_keywords': career_keywords,
            'job_data': job_data,
            'analysis': analysis,
            'insights': insights,
            'processed_at': datetime.now().isoformat()
        }
    
    def _extract_career_keywords(self, query: str) -> List[str]:
        """Extract career-related keywords from query"""
        # Simple keyword extraction (in production, use NLP)
        keywords = []
        
        # Common career terms
        career_terms = [
            'data scientist', 'software engineer', 'data analyst',
            'machine learning engineer', 'product manager', 'consultant',
            'developer', 'analyst', 'engineer', 'manager'
        ]
        
        query_lower = query.lower()
        for term in career_terms:
            if term in query_lower:
                keywords.append(term)
        
        return keywords if keywords else ['data scientist']  # Default
    
    def _scrape_job_postings(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Autonomously scrape job postings"""
        job_postings = []
        
        for keyword in keywords:
            # Scrape Indeed
            indeed_jobs = self._scrape_indeed(keyword)
            job_postings.extend(indeed_jobs)
            
            # Scrape LinkedIn (simplified)
            linkedin_jobs = self._scrape_linkedin(keyword)
            job_postings.extend(linkedin_jobs)
        
        return job_postings
    
    def _scrape_indeed(self, keyword: str) -> List[Dict[str, Any]]:
        """Scrape Indeed job postings"""
        jobs = []
        
        try:
            # Indeed search URL
            url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l="
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job listings (simplified)
                job_cards = soup.find_all('div', {'data-testid': 'job-card'})
                
                for card in job_cards[:10]:  # Limit to 10 jobs
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        
                        if title_elem and company_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                                'source': 'Indeed',
                                'keyword': keyword,
                                'scraped_at': datetime.now().isoformat()
                            }
                            jobs.append(job)
                    except Exception as e:
                        print(f"Error parsing Indeed job: {e}")
                        continue
        
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        
        return jobs
    
    def _scrape_linkedin(self, keyword: str) -> List[Dict[str, Any]]:
        """Scrape LinkedIn job postings (simplified)"""
        jobs = []
        
        try:
            # LinkedIn search URL (simplified)
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job listings (simplified)
                job_cards = soup.find_all('div', class_='job-search-card')
                
                for card in job_cards[:10]:  # Limit to 10 jobs
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        
                        if title_elem and company_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else 'N/A',
                                'source': 'LinkedIn',
                                'keyword': keyword,
                                'scraped_at': datetime.now().isoformat()
                            }
                            jobs.append(job)
                    except Exception as e:
                        print(f"Error parsing LinkedIn job: {e}")
                        continue
        
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
        
        return jobs
    
    def _analyze_market_trends(self, job_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze job market trends"""
        
        if not job_data:
            return {'error': 'No job data available'}
        
        # Extract skills and requirements
        all_skills = []
        companies = []
        locations = []
        
        for job in job_data:
            # Extract skills from job title and description
            title_skills = self._extract_skills_from_text(job['title'])
            all_skills.extend(title_skills)
            
            companies.append(job['company'])
            locations.append(job['location'])
        
        # Analyze trends
        skill_frequency = {}
        for skill in all_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        top_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'total_jobs': len(job_data),
            'top_skills': top_skills,
            'companies': list(set(companies)),
            'locations': list(set(locations)),
            'skill_frequency': skill_frequency
        }
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text"""
        skills = []
        
        # Common tech skills
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'SQL', 'R', 'Machine Learning',
            'Data Analysis', 'AWS', 'Docker', 'Kubernetes', 'React',
            'Node.js', 'TensorFlow', 'Pandas', 'NumPy', 'Scikit-learn'
        ]
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        return skills
    
    def _generate_insights(self, analysis: Dict[str, Any], query: str) -> str:
        """Generate insights based on analysis"""
        
        if 'error' in analysis:
            return f"Unable to analyze job market data: {analysis['error']}"
        
        insights = f"""
        **Job Market Analysis for: {query}**
        
        **Market Overview:**
        - Total jobs analyzed: {analysis['total_jobs']}
        - Companies hiring: {len(analysis['companies'])}
        - Locations: {len(analysis['locations'])}
        
        **Top Required Skills:**
        """
        
        for i, (skill, count) in enumerate(analysis['top_skills'][:5], 1):
            insights += f"{i}. {skill} (appears in {count} jobs)\n"
        
        insights += f"""
        
        **Key Insights:**
        - The job market shows strong demand for {query} roles
        - Top skills in demand: {', '.join([skill for skill, _ in analysis['top_skills'][:3]])}
        - Companies actively hiring: {', '.join(analysis['companies'][:3])}
        
        **Recommendations:**
        - Focus on developing the top 3 skills identified
        - Consider opportunities in the locations with most job postings
        - Research the companies that are actively hiring
        """
        
        return insights
