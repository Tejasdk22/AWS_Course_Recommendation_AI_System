"""
Course Catalog Agent for AWS Course Recommendation AI System
Crawls UTD course catalog to extract course information and skill mappings
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
import re as regex
try:
    from .base_agent import BaseAgent
except ImportError:
    from base_agent import BaseAgent


class CourseCatalogAgent(BaseAgent):
    """
    Agent responsible for fetching and analyzing course catalog data
    from UTD and other educational institutions.
    """
    
    def __init__(self):
        super().__init__("CourseCatalogAgent")
        
        # Major to UTD catalog URL mapping
        self.major_catalog_mapping = {
            # Graduate programs
            'business analytics': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/business-analytics',
                'undergraduate': None,
                'doctoral': None
            },
            'information technology and management': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/information-technology-management',
                'undergraduate': None,
                'doctoral': None
            },
            'accounting': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/accounting',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/jsom/accounting',
                'doctoral': None
            },
            'finance': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/finance',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/jsom/finance',
                'doctoral': None
            },
            'marketing': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/marketing',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/jsom/marketing',
                'doctoral': None
            },
            'supply chain management': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/supply-chain-management',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/jsom/supply-chain-management',
                'doctoral': None
            },
            'management information systems': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/jsom/information-systems',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/jsom/information-systems',
                'doctoral': None
            },
            'computer science': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/computer-science',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/ecs/computer-science',
                'doctoral': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/computer-science'
            },
            'software engineering': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/software-engineering',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/ecs/software-engineering',
                'doctoral': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/software-engineering'
            },
            'electrical engineering': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/electrical-engineering',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/ecs/electrical-engineering',
                'doctoral': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/electrical-engineering'
            },
            'cybersecurity': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/ecs/cybersecurity',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/ecs/cybersecurity',
                'doctoral': None
            },
            'data science': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/data-science-statistics',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/nsm/data-science',
                'doctoral': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/data-science-statistics'
            },
            'data science and statistics': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/data-science-statistics',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/nsm/data-science',
                'doctoral': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/data-science-statistics'
            },
            'mathematics': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/mathematics',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/nsm/mathematics',
                'doctoral': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/mathematics'
            },
            'statistics': {
                'graduate': 'https://catalog.utdallas.edu/2025/graduate/programs/nsm/statistics',
                'undergraduate': 'https://catalog.utdallas.edu/2025/undergraduate/programs/nsm/statistics',
                'doctoral': None
            }
        }
        
        self.course_sites = {
            'utd': {
                'base_url': 'https://catalog.utdallas.edu',
                'undergraduate_path': '/2025/undergraduate/courses',
                'graduate_path': '/2025/graduate/courses',
                'departments': [
                    'CS', 'SE', 'EE', 'CE', 'MATH', 'STAT', 'ATEC', 'IS'
                ]
            }
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.delay_between_requests = 1  # seconds
        self.max_courses_per_department = 50
        self.current_major = None
        self.current_student_type = None
        
        # Major-specific allowed course prefixes
        # Students can only take courses within their major's allowed prefixes
        # Note: ITSS is undergraduate-level; graduate ITM students use MIS, SYSM, ITM
        self.major_allowed_prefixes = {
            'business analytics': ['BUAN', 'MIS', 'OPRE'],
            'information technology and management': ['MIS', 'IMS', 'OPRE', 'FIN', 'ACCT', 'MKT', 'ENTP', 'OB', 'HMGT', 'BPS', 'MECO', 'REAL'],
            'computer science': ['CS', 'SE', 'CE'],
            'software engineering': ['SE', 'CS', 'CE'],
            'electrical engineering': ['EE', 'CE', 'CS'],
            'cybersecurity': ['CS', 'CE'],
            'management information systems': ['MIS', 'BUAN'],
            'accounting': ['ACCT', 'OPRE'],
            'finance': ['FIN', 'OPRE'],
            'marketing': ['MKT', 'OPRE'],
            'supply chain management': ['SCM', 'OPRE', 'SYSM'],
        }
    
    async def fetch_data(self, major: str = None, student_type: str = None) -> List[Dict[str, Any]]:
        """
        Fetch course catalog data from UTD and other sources.
        
        Args:
            major: Student's major (optional)
            student_type: Student type - 'graduate' or 'undergraduate' (optional)
        
        Returns:
            List of courses from all sources
        """
        self.current_major = major
        self.current_student_type = student_type
        
        self.logger.info(f"Starting course catalog data fetch for major: {major}, type: {student_type}")
        
        all_courses = []
        
        async with aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            # If we have a specific major and student type, fetch from specific URL
            if major and student_type:
                major_lower = major.lower()
                if major_lower in self.major_catalog_mapping:
                    catalog_url = self.major_catalog_mapping[major_lower].get(student_type.lower())
                    if catalog_url:
                        self.logger.info(f"Fetching courses from major-specific URL: {catalog_url}")
                        try:
                            async with session.get(catalog_url) as response:
                                if response.status == 200:
                                    html = await response.text()
                                    level_courses = self._parse_utd_courses(html, student_type.lower())
                                    all_courses.extend(level_courses)
                                    self.logger.info(f"Fetched {len(level_courses)} courses from {catalog_url}")
                                else:
                                    self.logger.warning(f"Failed to fetch courses from {catalog_url}: {response.status}")
                        except Exception as e:
                            self.logger.error(f"Error fetching courses from {catalog_url}: {e}")
            
            # Fallback to general catalog if no major-specific courses found
            if not all_courses:
                tasks = []
                
                # Create tasks for each course site
                for site_name, site_config in self.course_sites.items():
                    task = self._fetch_courses_from_site(session, site_name, site_config)
                    tasks.append(task)
                
                # Execute all tasks concurrently
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Combine results
                for result in results:
                    if isinstance(result, Exception):
                        self.logger.error(f"Error fetching courses: {result}")
                    elif isinstance(result, list):
                        all_courses.extend(result)
        
        self.logger.info(f"Fetched {len(all_courses)} total courses")
        return all_courses
    
    async def _fetch_courses_from_site(self, session: aiohttp.ClientSession, 
                                     site_name: str, site_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch courses from a specific site.
        
        Args:
            session: aiohttp session
            site_name: Name of the course site
            site_config: Configuration for the site
            
        Returns:
            List of courses from the site
        """
        courses = []
        
        try:
            if site_name == 'utd':
                courses = await self._fetch_utd_courses(session, site_config)
        except Exception as e:
            self.logger.error(f"Error fetching from {site_name}: {e}")
        
        return courses
    
    async def _fetch_utd_courses(self, session: aiohttp.ClientSession, 
                               site_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch courses from UTD catalog."""
        courses = []
        
        # Fetch both undergraduate and graduate courses
        for level in ['undergraduate', 'graduate']:
            level_path = site_config.get(f'{level}_path')
            if not level_path:
                continue
            
            url = f"{site_config['base_url']}{level_path}"
            self.logger.info(f"Fetching UTD {level} courses from: {url}")
            
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        level_courses = self._parse_utd_courses(html, level)
                        courses.extend(level_courses)
                        
                        # Rate limiting
                        await asyncio.sleep(self.delay_between_requests)
                    else:
                        self.logger.warning(f"Failed to fetch UTD {level} courses: {response.status}")
            except Exception as e:
                self.logger.error(f"Error fetching UTD {level} courses: {e}")
        
        return courses
    
    def _parse_utd_courses(self, html: str, level: str) -> List[Dict[str, Any]]:
        """
        Parse UTD courses from HTML content.
        
        Args:
            html: HTML content to parse
            level: Course level (undergraduate/graduate)
            
        Returns:
            List of parsed courses
        """
        soup = BeautifulSoup(html, 'html.parser')
        courses = []
        
        # Look for course blocks - UTD catalog structure
        course_blocks = soup.find_all('div', class_='courseblock') or \
                       soup.find_all('div', class_='course') or \
                       soup.find_all('div', {'data-course': True})
        
        for block in course_blocks:
            try:
                course = self._extract_utd_course_info(block, level)
                if course:
                    courses.append(course)
            except Exception as e:
                self.logger.warning(f"Error parsing UTD course block: {e}")
                continue
        
        # If no course blocks found, try alternative parsing
        if not courses:
            courses = self._parse_utd_courses_alternative(soup, level)
        
        return courses[:self.max_courses_per_department]  # Limit courses per department
    
    def _extract_utd_course_info(self, block: BeautifulSoup, level: str) -> Optional[Dict[str, Any]]:
        """Extract course information from UTD course block."""
        try:
            # Course code and title
            title_elem = block.find('h3', class_='courseblocktitle') or \
                        block.find('span', class_='courseblocktitle') or \
                        block.find('h3')
            
            if not title_elem:
                return None
            
            title_text = title_elem.get_text(strip=True)
            
            # Extract course code and title
            course_match = re.match(r'^([A-Z]{2,4}\s*\d{4,5}[A-Z]?)\s*(.+)$', title_text)
            if not course_match:
                return None
            
            course_code = course_match.group(1).strip()
            course_title = course_match.group(2).strip()
            
            # Description
            desc_elem = block.find('p', class_='courseblockdesc') or \
                       block.find('div', class_='courseblockdesc') or \
                       block.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Prerequisites
            prereq_elem = block.find('p', class_='prereq') or \
                         block.find('span', class_='prereq')
            prerequisites = prereq_elem.get_text(strip=True) if prereq_elem else ""
            
            # Extract skills from description and title
            skills = self._extract_skills_from_course(description, course_title, course_code)
            
            # Determine department
            department = course_code.split()[0] if ' ' in course_code else course_code[:2]
            
            return {
                'course_code': course_code,
                'course_title': course_title,
                'description': description,
                'prerequisites': prerequisites,
                'skills': skills,
                'department': department,
                'level': level,
                'source': 'UTD',
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.warning(f"Error extracting UTD course info: {e}")
            return None
    
    def _parse_utd_courses_alternative(self, soup: BeautifulSoup, level: str) -> List[Dict[str, Any]]:
        """Alternative parsing method for UTD courses."""
        courses = []
        
        # Look for any text that matches course patterns
        text_content = soup.get_text()
        course_pattern = r'([A-Z]{2,4}\s*\d{4,5}[A-Z]?)\s+([^.\n]+)'
        matches = re.finditer(course_pattern, text_content)
        
        for match in matches:
            course_code = match.group(1).strip()
            course_title = match.group(2).strip()
            
            # Extract skills
            skills = self._extract_skills_from_course("", course_title, course_code)
            
            courses.append({
                'course_code': course_code,
                'course_title': course_title,
                'description': "",
                'prerequisites': "",
                'skills': skills,
                'department': course_code.split()[0] if ' ' in course_code else course_code[:2],
                'level': level,
                'source': 'UTD',
                'scraped_at': datetime.now().isoformat()
            })
        
        return courses[:self.max_courses_per_department]
    
    def _extract_skills_from_course(self, description: str, title: str, course_code: str) -> List[str]:
        """
        Extract relevant skills from course information.
        
        Args:
            description: Course description
            title: Course title
            course_code: Course code
            
        Returns:
            List of extracted skills
        """
        # Combine all text for skill extraction
        full_text = f"{title} {description} {course_code}".lower()
        
        # Comprehensive skill keywords for data science and related fields
        skill_keywords = {
            # Programming Languages
            'Python': ['python', 'py'],
            'Java': ['java', 'javase', 'j2ee'],
            'C++': ['c++', 'cpp', 'c plus plus'],
            'C': ['c programming', 'c language'],
            'JavaScript': ['javascript', 'js', 'node.js', 'nodejs'],
            'TypeScript': ['typescript', 'ts'],
            'R': ['r programming', 'r language', 'r statistical'],
            'SQL': ['sql', 'database', 'mysql', 'postgresql'],
            'Scala': ['scala'],
            'Go': ['golang', 'go language'],
            'Rust': ['rust'],
            'MATLAB': ['matlab'],
            'Julia': ['julia'],
            
            # Data Science & ML
            'Machine Learning': ['machine learning', 'ml', 'supervised learning', 'unsupervised learning'],
            'Deep Learning': ['deep learning', 'neural networks', 'cnn', 'rnn', 'lstm'],
            'Data Analysis': ['data analysis', 'data analytics', 'statistical analysis'],
            'Data Visualization': ['data visualization', 'visualization', 'plotting', 'charts'],
            'Statistics': ['statistics', 'statistical', 'probability', 'inference'],
            'Artificial Intelligence': ['artificial intelligence', 'ai', 'intelligent systems'],
            'Natural Language Processing': ['nlp', 'natural language processing', 'text processing'],
            'Computer Vision': ['computer vision', 'image processing', 'cv'],
            'Big Data': ['big data', 'large scale data', 'distributed computing'],
            'Data Mining': ['data mining', 'pattern recognition', 'knowledge discovery'],
            
            # Tools & Frameworks
            'TensorFlow': ['tensorflow', 'tf'],
            'PyTorch': ['pytorch', 'torch'],
            'Scikit-learn': ['scikit-learn', 'sklearn', 'scikit learn'],
            'Pandas': ['pandas', 'dataframe'],
            'NumPy': ['numpy', 'numerical python'],
            'Matplotlib': ['matplotlib', 'plotting'],
            'Seaborn': ['seaborn', 'statistical visualization'],
            'Jupyter': ['jupyter', 'notebook', 'jupyter notebook'],
            'RStudio': ['rstudio', 'r studio'],
            'Tableau': ['tableau'],
            'Power BI': ['power bi', 'powerbi'],
            'Apache Spark': ['spark', 'apache spark', 'pyspark'],
            'Hadoop': ['hadoop', 'hdfs', 'mapreduce'],
            'Kafka': ['kafka', 'apache kafka'],
            
            # Cloud & Infrastructure
            'AWS': ['aws', 'amazon web services', 'amazon cloud'],
            'Azure': ['azure', 'microsoft azure'],
            'GCP': ['gcp', 'google cloud', 'google cloud platform'],
            'Docker': ['docker', 'containerization'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'Git': ['git', 'version control'],
            'GitHub': ['github', 'git hub'],
            'CI/CD': ['ci/cd', 'continuous integration', 'continuous deployment'],
            'MLOps': ['mlops', 'ml ops', 'machine learning operations'],
            
            # Databases
            'PostgreSQL': ['postgresql', 'postgres'],
            'MySQL': ['mysql'],
            'MongoDB': ['mongodb', 'mongo'],
            'Redis': ['redis'],
            'Elasticsearch': ['elasticsearch', 'elastic search'],
            
            # Software Engineering
            'Software Engineering': ['software engineering', 'software development'],
            'Object-Oriented Programming': ['oop', 'object oriented', 'object-oriented'],
            'Design Patterns': ['design patterns', 'software patterns'],
            'Agile': ['agile', 'scrum', 'sprint'],
            'Testing': ['testing', 'unit testing', 'integration testing'],
            'API Development': ['api', 'rest api', 'web services'],
            'Microservices': ['microservices', 'micro services'],
            
            # Mathematics
            'Linear Algebra': ['linear algebra', 'matrix', 'vector'],
            'Calculus': ['calculus', 'derivatives', 'integrals'],
            'Discrete Mathematics': ['discrete math', 'discrete mathematics'],
            'Probability': ['probability', 'probabilistic'],
            'Optimization': ['optimization', 'optimization theory'],
            'Graph Theory': ['graph theory', 'graphs', 'networks'],
            
            # Domain Specific
            'Cybersecurity': ['cybersecurity', 'security', 'cyber security'],
            'Blockchain': ['blockchain', 'cryptocurrency', 'crypto'],
            'IoT': ['iot', 'internet of things'],
            'Robotics': ['robotics', 'robotic systems'],
            'Game Development': ['game development', 'game programming'],
            'Web Development': ['web development', 'web programming', 'frontend', 'backend'],
            'Mobile Development': ['mobile development', 'ios', 'android', 'react native'],
        }
        
        found_skills = []
        
        for skill, keywords in skill_keywords.items():
            for keyword in keywords:
                if keyword in full_text:
                    found_skills.append(skill)
                    break  # Avoid duplicate skills
        
        return list(set(found_skills))  # Remove duplicates
    
    def _filter_courses_by_prefix(self, courses: List[Dict[str, Any]], major: str = None) -> List[Dict[str, Any]]:
        """
        Filter courses to only include those with allowed prefixes for the major.
        
        Args:
            courses: List of course dictionaries
            major: Student's major (optional)
            
        Returns:
            Filtered list of courses
        """
        if not major or not courses:
            return courses
        
        major_lower = major.lower()
        allowed_prefixes = self.major_allowed_prefixes.get(major_lower, [])
        
        if not allowed_prefixes:
            # If no specific prefixes defined, return all courses
            return courses
        
        filtered_courses = []
        for course in courses:
            course_code = course.get('course_code', '')
            # Extract prefix (first part before space or number)
            # Handle both "BUAN 6345" (with space) and "BUAN6345" (no space) formats
            if ' ' in course_code:
                prefix_match = course_code.split()[0]
            else:
                # Extract letters before numbers, e.g., "BUAN6345" -> "BUAN"
                prefix_match = regex.match(r'^([A-Z]+)', course_code.upper())
                prefix_match = prefix_match.group(1) if prefix_match else course_code[:4]
            
            if any(allowed.upper() == prefix_match.upper() for allowed in allowed_prefixes):
                filtered_courses.append(course)
            else:
                self.logger.debug(f"Filtering out course {course_code} - prefix '{prefix_match}' not in allowed prefixes {allowed_prefixes} for {major}")
        
        self.logger.info(f"Filtered {len(courses)} courses to {len(filtered_courses)} for major {major} (allowed prefixes: {allowed_prefixes})")
        return filtered_courses
    
    def _filter_courses_by_level(self, courses: List[Dict[str, Any]], student_type: str) -> List[Dict[str, Any]]:
        """
        Filter courses to only include courses appropriate for the student type.
        
        Args:
            courses: List of course dictionaries
            student_type: Student type (undergraduate/graduate/doctoral)
            
        Returns:
            Filtered list of courses by level
        """
        if not student_type or not courses:
            return courses
        
        student_type_lower = student_type.lower()
        filtered_courses = []
        
        for course in courses:
            course_level = course.get('level', '').lower()
            
            # Check if course level matches student type
            if student_type_lower == 'undergraduate':
                # Undergraduate students can only see undergraduate courses
                if course_level in ['undergraduate', 'both', '']:
                    filtered_courses.append(course)
                else:
                    self.logger.debug(f"Filtering out {course.get('course_code')} - level '{course_level}' not for undergraduate")
            elif student_type_lower == 'graduate':
                # Graduate students can only see graduate courses
                if course_level in ['graduate', 'both', '']:
                    filtered_courses.append(course)
                else:
                    self.logger.debug(f"Filtering out {course.get('course_code')} - level '{course_level}' not for graduate")
            elif student_type_lower == 'doctoral':
                # Doctoral students can see graduate and doctoral courses
                if course_level in ['doctoral', 'graduate', 'both', '']:
                    filtered_courses.append(course)
                else:
                    self.logger.debug(f"Filtering out {course.get('course_code')} - level '{course_level}' not for doctoral")
            else:
                # Unknown student type, include all courses
                filtered_courses.append(course)
        
        self.logger.info(f"Filtered {len(courses)} courses to {len(filtered_courses)} for student type {student_type}")
        return filtered_courses
    
    def process_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process and analyze course catalog data.
        
        Args:
            data: Raw course data
            
        Returns:
            Processed course catalog analysis
        """
        self.logger.info(f"Processing {len(data)} courses")
        
        # Filter courses based on major's allowed prefixes and student type
        if self.current_major:
            data = self._filter_courses_by_prefix(data, self.current_major)
        
        # Filter by student type level (undergraduate vs graduate vs doctoral)
        if self.current_student_type:
            data = self._filter_courses_by_level(data, self.current_student_type)
        
        if not data:
            return {
                'total_courses': 0,
                'skills_analysis': {},
                'department_analysis': {},
                'level_analysis': {},
                'course_skills_mapping': {},
                'processed_at': datetime.now().isoformat()
            }
        
        # Extract all skills
        all_skills = []
        for course in data:
            all_skills.extend(course.get('skills', []))
        
        # Skills frequency analysis
        skills_freq = {}
        for skill in all_skills:
            skills_freq[skill] = skills_freq.get(skill, 0) + 1
        
        # Sort skills by frequency
        top_skills = sorted(skills_freq.items(), key=lambda x: x[1], reverse=True)[:30]
        
        # Department analysis
        departments = [course.get('department', 'Unknown') for course in data]
        dept_freq = {}
        for dept in departments:
            dept_freq[dept] = dept_freq.get(dept, 0) + 1
        
        # Level analysis
        levels = [course.get('level', 'Unknown') for course in data]
        level_freq = {}
        for level in levels:
            level_freq[level] = level_freq.get(level, 0) + 1
        
        # Create course-to-skills mapping
        course_skills_mapping = {}
        for course in data:
            course_code = course.get('course_code', 'Unknown')
            skills = course.get('skills', [])
            course_skills_mapping[course_code] = {
                'title': course.get('course_title', ''),
                'skills': skills,
                'department': course.get('department', ''),
                'level': course.get('level', '')
            }
        
        # Create skills-to-courses mapping
        skills_courses_mapping = {}
        for course in data:
            course_code = course.get('course_code', 'Unknown')
            skills = course.get('skills', [])
            for skill in skills:
                if skill not in skills_courses_mapping:
                    skills_courses_mapping[skill] = []
                skills_courses_mapping[skill].append(course_code)
        
        processed_data = {
            'total_courses': len(data),
            'skills_analysis': {
                'top_skills': top_skills,
                'total_unique_skills': len(skills_freq),
                'skills_frequency': dict(top_skills)
            },
            'department_analysis': {
                'top_departments': sorted(dept_freq.items(), key=lambda x: x[1], reverse=True),
                'total_departments': len(dept_freq)
            },
            'level_analysis': {
                'level_distribution': dict(level_freq),
                'total_levels': len(level_freq)
            },
            'course_skills_mapping': course_skills_mapping,
            'skills_courses_mapping': skills_courses_mapping,
            'raw_courses': data,
            'processed_at': datetime.now().isoformat()
        }
        
        self.logger.info("Course catalog data processing completed")
        return processed_data
    
    async def respond(self, processed_data: Dict[str, Any], user_query: str = None) -> str:
        """
        Generate a response based on processed course catalog data.
        
        Args:
            processed_data: Processed course catalog analysis
            user_query: Optional user query for context
            
        Returns:
            Generated response about available courses
        """
        if not processed_data or processed_data.get('total_courses', 0) == 0:
            return "No course catalog data available to analyze."
        
        # Save processed data
        self.save_data(processed_data, 'course_catalog_analysis.json')
        
        # Generate response using Bedrock
        prompt = self._create_course_catalog_prompt(processed_data, user_query)
        response = await self.invoke_bedrock(prompt)
        
        return response
    
    def _create_course_catalog_prompt(self, data: Dict[str, Any], user_query: str = None) -> str:
        """Create a prompt for course catalog analysis."""
        
        skills_analysis = data.get('skills_analysis', {})
        department_analysis = data.get('department_analysis', {})
        level_analysis = data.get('level_analysis', {})
        
        prompt = f"""
        As a career guidance AI, analyze the following course catalog data:

        **Course Catalog Overview:**
        - Total courses analyzed: {data.get('total_courses', 0)}
        - Analysis date: {data.get('processed_at', 'N/A')}

        **Top Skills Covered:**
        {self._format_skills_list(skills_analysis.get('top_skills', []))}

        **Department Distribution:**
        {self._format_department_list(department_analysis.get('top_departments', []))}

        **Level Distribution:**
        {self._format_level_list(level_analysis.get('level_distribution', {}))}

        **User Query:** {user_query or 'General course catalog analysis'}

        Please provide:
        1. Overview of available courses and their skill coverage
        2. Most commonly taught skills and technologies
        3. Department-wise course distribution
        4. Recommendations for course selection based on career goals
        5. Skill gaps that could be filled with specific courses

        Format your response in a clear, actionable manner suitable for career guidance.
        """
        
        return prompt
    
    def _format_skills_list(self, skills: List[tuple]) -> str:
        """Format skills list for display."""
        if not skills:
            return "No skills data available"
        
        formatted = []
        for i, (skill, count) in enumerate(skills[:15], 1):
            formatted.append(f"{i}. {skill} (covered in {count} courses)")
        
        return "\n".join(formatted)
    
    def _format_department_list(self, departments: List[tuple]) -> str:
        """Format departments list for display."""
        if not departments:
            return "No department data available"
        
        formatted = []
        for i, (dept, count) in enumerate(departments[:10], 1):
            formatted.append(f"{i}. {dept} ({count} courses)")
        
        return "\n".join(formatted)
    
    def _format_level_list(self, levels: Dict[str, int]) -> str:
        """Format levels list for display."""
        if not levels:
            return "No level data available"
        
        formatted = []
        for level, count in levels.items():
            formatted.append(f"- {level.title()}: {count} courses")
        
        return "\n".join(formatted)
    
    async def run(self, user_query: str = None, major: str = None, student_type: str = None) -> str:
        """
        Run the complete course catalog agent workflow with context.
        
        Args:
            user_query: Optional user query for context
            major: Student's major (optional)
            student_type: Student type - 'graduate' or 'undergraduate' (optional)
            
        Returns:
            Final response from the agent
        """
        try:
            self.logger.info(f"Starting {self.agent_name} workflow")
            
            # Fetch data with major and student type context
            raw_data = await self.fetch_data(major=major, student_type=student_type)
            if not raw_data:
                return "Error: No data fetched"
            
            # Process data
            processed_data = self.process_data(raw_data)
            if not processed_data:
                return "Error: Data processing failed"
            
            # Generate response
            response = await self.respond(processed_data, user_query)
            
            self.logger.info(f"{self.agent_name} workflow completed successfully")
            return response
            
        except Exception as e:
            self.logger.error(f"{self.agent_name} workflow failed: {e}")
            return f"Error: {self.agent_name} failed - {str(e)}"
