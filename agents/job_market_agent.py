"""
Job Market Agent for AWS Course Recommendation AI System
Scrapes job postings from LinkedIn and Indeed to analyze market trends
"""

import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime
try:
    from .base_agent import BaseAgent
except ImportError:
    from base_agent import BaseAgent


class JobMarketAgent(BaseAgent):
    """
    Agent responsible for fetching and analyzing job market data
    from various job posting websites.
    """
    
    def __init__(self):
        super().__init__("JobMarketAgent")
        self.job_sites = {
            'indeed': {
                'base_url': 'https://www.indeed.com',
                'search_path': '/jobs',
                'params': {
                    'q': 'data scientist',
                    'l': '',
                    'sort': 'date',
                    'fromage': '7'  # Last 7 days
                }
            },
            'linkedin': {
                'base_url': 'https://www.linkedin.com',
                'search_path': '/jobs/search',
                'params': {
                    'keywords': 'data scientist',
                    'locationId': '',
                    'f_TPR': 'r604800'  # Last 7 days
                }
            }
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.max_pages = 3
        self.delay_between_requests = 1  # seconds
    
    async def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetch job postings from multiple job sites asynchronously.
        
        Returns:
            List of job postings from all sources
        """
        self.logger.info("Starting job market data fetch")
        
        all_jobs = []
        
        async with aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            tasks = []
            
            # Create tasks for each job site
            for site_name, site_config in self.job_sites.items():
                task = self._fetch_jobs_from_site(session, site_name, site_config)
                tasks.append(task)
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            for result in results:
                if isinstance(result, Exception):
                    self.logger.error(f"Error fetching jobs: {result}")
                elif isinstance(result, list):
                    all_jobs.extend(result)
        
        self.logger.info(f"Fetched {len(all_jobs)} total job postings")
        return all_jobs
    
    async def _fetch_jobs_from_site(self, session: aiohttp.ClientSession, 
                                  site_name: str, site_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch jobs from a specific site.
        
        Args:
            session: aiohttp session
            site_name: Name of the job site
            site_config: Configuration for the site
            
        Returns:
            List of job postings from the site
        """
        jobs = []
        
        try:
            for page in range(self.max_pages):
                # Build URL with pagination
                if page > 0:
                    site_config['params']['start'] = str(page * 10)
                
                url = self._build_url(site_config)
                self.logger.info(f"Fetching {site_name} page {page + 1}: {url}")
                
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        page_jobs = self._parse_jobs_from_html(html, site_name)
                        jobs.extend(page_jobs)
                        
                        # Rate limiting
                        await asyncio.sleep(self.delay_between_requests)
                    else:
                        self.logger.warning(f"Failed to fetch {site_name} page {page + 1}: {response.status}")
                        
        except Exception as e:
            self.logger.error(f"Error fetching from {site_name}: {e}")
        
        return jobs
    
    def _build_url(self, site_config: Dict[str, Any]) -> str:
        """Build the complete URL for job search."""
        base_url = site_config['base_url']
        search_path = site_config['search_path']
        params = site_config['params']
        
        # Build query string
        query_parts = []
        for key, value in params.items():
            if value:
                query_parts.append(f"{key}={value}")
        
        query_string = "&".join(query_parts)
        return f"{base_url}{search_path}?{query_string}"
    
    def _parse_jobs_from_html(self, html: str, site_name: str) -> List[Dict[str, Any]]:
        """
        Parse job postings from HTML content.
        
        Args:
            html: HTML content to parse
            site_name: Name of the site for site-specific parsing
            
        Returns:
            List of parsed job postings
        """
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        if site_name == 'indeed':
            jobs = self._parse_indeed_jobs(soup)
        elif site_name == 'linkedin':
            jobs = self._parse_linkedin_jobs(soup)
        
        return jobs
    
    def _parse_indeed_jobs(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse Indeed job postings."""
        jobs = []
        
        # Indeed job card selectors (these may need updating based on current site structure)
        job_cards = soup.find_all('div', {'data-testid': 'job-card'}) or \
                   soup.find_all('div', class_='job_seen_beacon') or \
                   soup.find_all('div', class_='jobsearch-SerpJobCard')
        
        for card in job_cards:
            try:
                job = self._extract_job_info_indeed(card)
                if job:
                    jobs.append(job)
            except Exception as e:
                self.logger.warning(f"Error parsing Indeed job card: {e}")
                continue
        
        return jobs
    
    def _parse_linkedin_jobs(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse LinkedIn job postings."""
        jobs = []
        
        # LinkedIn job card selectors
        job_cards = soup.find_all('div', class_='job-search-card') or \
                   soup.find_all('div', {'data-entity-urn': True})
        
        for card in job_cards:
            try:
                job = self._extract_job_info_linkedin(card)
                if job:
                    jobs.append(job)
            except Exception as e:
                self.logger.warning(f"Error parsing LinkedIn job card: {e}")
                continue
        
        return jobs
    
    def _extract_job_info_indeed(self, card: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """Extract job information from Indeed job card."""
        try:
            # Title
            title_elem = card.find('h2', class_='jobTitle') or card.find('a', {'data-testid': 'job-title'})
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Company
            company_elem = card.find('span', class_='companyName') or card.find('a', {'data-testid': 'company-name'})
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Location
            location_elem = card.find('div', class_='companyLocation') or card.find('div', {'data-testid': 'job-location'})
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Salary
            salary_elem = card.find('span', class_='salaryText') or card.find('div', {'data-testid': 'attribute_snippet_testid'})
            salary = salary_elem.get_text(strip=True) if salary_elem else "N/A"
            
            # Description snippet
            desc_elem = card.find('div', class_='summary') or card.find('div', {'data-testid': 'job-snippet'})
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Extract skills from description
            skills = self._extract_skills_from_text(description)
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
                'skills': skills,
                'source': 'Indeed',
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.warning(f"Error extracting Indeed job info: {e}")
            return None
    
    def _extract_job_info_linkedin(self, card: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """Extract job information from LinkedIn job card."""
        try:
            # Title
            title_elem = card.find('h3', class_='base-search-card__title') or card.find('a', class_='base-card__full-link')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Company
            company_elem = card.find('h4', class_='base-search-card__subtitle') or card.find('a', class_='hidden-nested-link')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Location
            location_elem = card.find('span', class_='job-search-card__location')
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Description snippet
            desc_elem = card.find('p', class_='job-search-card__snippet')
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Extract skills from description
            skills = self._extract_skills_from_text(description)
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'salary': "N/A",  # LinkedIn doesn't show salary in search results
                'description': description,
                'skills': skills,
                'source': 'LinkedIn',
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.warning(f"Error extracting LinkedIn job info: {e}")
            return None
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract relevant skills from job description text.
        
        Args:
            text: Job description text
            
        Returns:
            List of extracted skills
        """
        # Common data science and tech skills
        skill_keywords = [
            'Python', 'R', 'SQL', 'Java', 'Scala', 'JavaScript', 'TypeScript',
            'Machine Learning', 'Deep Learning', 'AI', 'Artificial Intelligence',
            'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy',
            'Data Analysis', 'Data Visualization', 'Tableau', 'Power BI', 'Matplotlib',
            'Seaborn', 'Plotly', 'D3.js', 'Statistics', 'Statistical Analysis',
            'A/B Testing', 'Hypothesis Testing', 'Regression', 'Classification',
            'Clustering', 'NLP', 'Natural Language Processing', 'Computer Vision',
            'Big Data', 'Hadoop', 'Spark', 'Kafka', 'AWS', 'Azure', 'GCP',
            'Docker', 'Kubernetes', 'Git', 'GitHub', 'CI/CD', 'MLOps',
            'Data Engineering', 'ETL', 'Data Pipeline', 'Data Warehouse',
            'Database', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
            'Cloud Computing', 'Serverless', 'Lambda', 'S3', 'Redshift',
            'Jupyter', 'Notebook', 'RStudio', 'IDE', 'VS Code',
            'Agile', 'Scrum', 'Project Management', 'Leadership'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def process_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process and analyze job market data.
        
        Args:
            data: Raw job postings data
            
        Returns:
            Processed job market analysis
        """
        self.logger.info(f"Processing {len(data)} job postings")
        
        if not data:
            return {
                'total_jobs': 0,
                'skills_analysis': {},
                'salary_analysis': {},
                'location_analysis': {},
                'company_analysis': {},
                'processed_at': datetime.now().isoformat()
            }
        
        # Extract all skills
        all_skills = []
        for job in data:
            all_skills.extend(job.get('skills', []))
        
        # Skills frequency analysis
        skills_freq = {}
        for skill in all_skills:
            skills_freq[skill] = skills_freq.get(skill, 0) + 1
        
        # Sort skills by frequency
        top_skills = sorted(skills_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Salary analysis
        salaries = []
        for job in data:
            salary = job.get('salary', 'N/A')
            if salary != 'N/A' and salary:
                # Extract numeric values from salary strings
                salary_nums = re.findall(r'[\d,]+', salary.replace(',', ''))
                if salary_nums:
                    try:
                        # Take the first number found
                        salary_val = int(salary_nums[0])
                        salaries.append(salary_val)
                    except ValueError:
                        continue
        
        # Location analysis
        locations = [job.get('location', 'N/A') for job in data]
        location_freq = {}
        for loc in locations:
            if loc != 'N/A':
                location_freq[loc] = location_freq.get(loc, 0) + 1
        
        # Company analysis
        companies = [job.get('company', 'N/A') for job in data]
        company_freq = {}
        for company in companies:
            if company != 'N/A':
                company_freq[company] = company_freq.get(company, 0) + 1
        
        processed_data = {
            'total_jobs': len(data),
            'skills_analysis': {
                'top_skills': top_skills,
                'total_unique_skills': len(skills_freq),
                'skills_frequency': dict(top_skills)
            },
            'salary_analysis': {
                'average_salary': sum(salaries) / len(salaries) if salaries else 0,
                'min_salary': min(salaries) if salaries else 0,
                'max_salary': max(salaries) if salaries else 0,
                'salary_count': len(salaries)
            },
            'location_analysis': {
                'top_locations': sorted(location_freq.items(), key=lambda x: x[1], reverse=True)[:10],
                'total_locations': len(location_freq)
            },
            'company_analysis': {
                'top_companies': sorted(company_freq.items(), key=lambda x: x[1], reverse=True)[:10],
                'total_companies': len(company_freq)
            },
            'raw_jobs': data,
            'processed_at': datetime.now().isoformat()
        }
        
        self.logger.info("Job market data processing completed")
        return processed_data
    
    async def respond(self, processed_data: Dict[str, Any], user_query: str = None) -> str:
        """
        Generate a response based on processed job market data.
        
        Args:
            processed_data: Processed job market analysis
            user_query: Optional user query for context
            
        Returns:
            Generated response about job market trends
        """
        if not processed_data or processed_data.get('total_jobs', 0) == 0:
            return "No job market data available to analyze."
        
        # Save processed data
        self.save_data(processed_data, 'job_market_analysis.json')
        
        # Generate response using Bedrock
        prompt = self._create_job_market_prompt(processed_data, user_query)
        response = await self.invoke_bedrock(prompt)
        
        return response
    
    def _create_job_market_prompt(self, data: Dict[str, Any], user_query: str = None) -> str:
        """Create a prompt for job market analysis."""
        
        skills_analysis = data.get('skills_analysis', {})
        salary_analysis = data.get('salary_analysis', {})
        location_analysis = data.get('location_analysis', {})
        
        prompt = f"""
        As a career guidance AI, analyze the following job market data for data science positions:

        **Job Market Overview:**
        - Total jobs analyzed: {data.get('total_jobs', 0)}
        - Analysis date: {data.get('processed_at', 'N/A')}

        **Top Required Skills:**
        {self._format_skills_list(skills_analysis.get('top_skills', []))}

        **Salary Information:**
        - Average salary: ${salary_analysis.get('average_salary', 0):,.0f}
        - Salary range: ${salary_analysis.get('min_salary', 0):,.0f} - ${salary_analysis.get('max_salary', 0):,.0f}
        - Jobs with salary data: {salary_analysis.get('salary_count', 0)}

        **Top Locations:**
        {self._format_location_list(location_analysis.get('top_locations', []))}

        **User Query:** {user_query or 'General job market analysis'}

        Please provide:
        1. Key insights about the current data science job market
        2. Most in-demand skills and their importance
        3. Salary trends and expectations
        4. Geographic distribution of opportunities
        5. Recommendations for job seekers

        Format your response in a clear, actionable manner suitable for career guidance.
        """
        
        return prompt
    
    def _format_skills_list(self, skills: List[tuple]) -> str:
        """Format skills list for display."""
        if not skills:
            return "No skills data available"
        
        formatted = []
        for i, (skill, count) in enumerate(skills[:10], 1):
            formatted.append(f"{i}. {skill} (appears in {count} jobs)")
        
        return "\n".join(formatted)
    
    def _format_location_list(self, locations: List[tuple]) -> str:
        """Format locations list for display."""
        if not locations:
            return "No location data available"
        
        formatted = []
        for i, (location, count) in enumerate(locations[:5], 1):
            formatted.append(f"{i}. {location} ({count} jobs)")
        
        return "\n".join(formatted)
