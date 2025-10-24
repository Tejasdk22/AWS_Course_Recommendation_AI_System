"""
AWS Lambda function for CourseCatalogAgent in Bedrock AgentCore
Autonomous UTD course catalog analysis agent
"""

import json
import boto3
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from datetime import datetime

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for CourseCatalogAgent
    Processes course catalog analysis requests autonomously
    """
    
    try:
        # Extract query from event
        query = event.get('query', '')
        session_id = event.get('sessionId', '')
        
        print(f"CourseCatalogAgent processing query: {query}")
        
        # Initialize agent
        agent = CourseCatalogAgent()
        
        # Process the query autonomously
        result = agent.process_course_catalog_query(query)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'CourseCatalogAgent',
                'query': query,
                'result': result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in CourseCatalogAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'CourseCatalogAgent'
            }
        }

class CourseCatalogAgent:
    """Autonomous UTD Course Catalog Analysis Agent"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'utd-career-guidance-data'
        self.utd_base_url = 'https://catalog.utdallas.edu'
        
    def process_course_catalog_query(self, query: str) -> Dict[str, Any]:
        """Process course catalog query autonomously"""
        
        # Extract course-related keywords from query
        course_keywords = self._extract_course_keywords(query)
        
        # Scrape UTD course catalog autonomously
        course_data = self._scrape_utd_courses(course_keywords)
        
        # Analyze course offerings
        analysis = self._analyze_course_offerings(course_data)
        
        # Generate recommendations
        recommendations = self._generate_course_recommendations(analysis, query)
        
        return {
            'course_keywords': course_keywords,
            'course_data': course_data,
            'analysis': analysis,
            'recommendations': recommendations,
            'processed_at': datetime.now().isoformat()
        }
    
    def _extract_course_keywords(self, query: str) -> List[str]:
        """Extract course-related keywords from query"""
        keywords = []
        
        # Common course terms
        course_terms = [
            'data science', 'machine learning', 'artificial intelligence',
            'software engineering', 'computer science', 'statistics',
            'mathematics', 'business', 'engineering', 'programming',
            'python', 'java', 'javascript', 'database', 'algorithms'
        ]
        
        query_lower = query.lower()
        for term in course_terms:
            if term in query_lower:
                keywords.append(term)
        
        return keywords if keywords else ['data science']  # Default
    
    def _scrape_utd_courses(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Autonomously scrape UTD course catalog"""
        courses = []
        
        # Scrape both undergraduate and graduate courses
        for level in ['undergraduate', 'graduate']:
            level_courses = self._scrape_utd_level_courses(level, keywords)
            courses.extend(level_courses)
        
        return courses
    
    def _scrape_utd_level_courses(self, level: str, keywords: List[str]) -> List[Dict[str, Any]]:
        """Scrape courses from specific level (undergraduate/graduate)"""
        courses = []
        
        try:
            # UTD catalog URL
            url = f"{self.utd_base_url}/2025/{level}/courses"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract course blocks
                course_blocks = soup.find_all('div', class_='courseblock')
                
                for block in course_blocks[:20]:  # Limit to 20 courses
                    try:
                        course = self._extract_course_info(block, level, keywords)
                        if course:
                            courses.append(course)
                    except Exception as e:
                        print(f"Error parsing course block: {e}")
                        continue
        
        except Exception as e:
            print(f"Error scraping UTD {level} courses: {e}")
        
        return courses
    
    def _extract_course_info(self, block, level: str, keywords: List[str]) -> Dict[str, Any]:
        """Extract course information from course block"""
        
        try:
            # Extract course title and code
            title_elem = block.find('h3', class_='courseblocktitle')
            if not title_elem:
                return None
            
            title_text = title_elem.get_text(strip=True)
            
            # Parse course code and title
            import re
            course_match = re.match(r'^([A-Z]{2,4}\s*\d{4,5}[A-Z]?)\s*(.+)$', title_text)
            if not course_match:
                return None
            
            course_code = course_match.group(1).strip()
            course_title = course_match.group(2).strip()
            
            # Extract description
            desc_elem = block.find('p', class_='courseblockdesc')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Extract prerequisites
            prereq_elem = block.find('p', class_='prereq')
            prerequisites = prereq_elem.get_text(strip=True) if prereq_elem else ""
            
            # Extract skills from description and title
            skills = self._extract_skills_from_course(description, course_title, course_code)
            
            # Check if course matches keywords
            matches_keywords = any(keyword.lower() in (description + course_title).lower() 
                                 for keyword in keywords)
            
            if matches_keywords or not keywords:  # Include if matches or no keywords specified
                return {
                    'course_code': course_code,
                    'course_title': course_title,
                    'description': description,
                    'prerequisites': prerequisites,
                    'skills': skills,
                    'level': level,
                    'source': 'UTD',
                    'scraped_at': datetime.now().isoformat()
                }
        
        except Exception as e:
            print(f"Error extracting course info: {e}")
        
        return None
    
    def _extract_skills_from_course(self, description: str, title: str, course_code: str) -> List[str]:
        """Extract skills from course information"""
        skills = []
        
        # Combine all text for skill extraction
        full_text = f"{title} {description} {course_code}".lower()
        
        # Comprehensive skill keywords
        skill_keywords = {
            'Python': ['python', 'py'],
            'Java': ['java', 'javase', 'j2ee'],
            'JavaScript': ['javascript', 'js', 'node.js'],
            'SQL': ['sql', 'database', 'mysql', 'postgresql'],
            'Machine Learning': ['machine learning', 'ml', 'supervised learning'],
            'Data Analysis': ['data analysis', 'data analytics', 'statistical analysis'],
            'Statistics': ['statistics', 'statistical', 'probability'],
            'Algorithms': ['algorithms', 'algorithm', 'data structures'],
            'Web Development': ['web development', 'html', 'css', 'react'],
            'Database': ['database', 'dbms', 'sql', 'nosql'],
            'AWS': ['aws', 'amazon web services', 'cloud'],
            'Docker': ['docker', 'containerization'],
            'Git': ['git', 'version control'],
            'Linear Algebra': ['linear algebra', 'matrix', 'vector'],
            'Calculus': ['calculus', 'derivatives', 'integrals'],
            'Discrete Math': ['discrete math', 'discrete mathematics'],
            'Software Engineering': ['software engineering', 'software development'],
            'Object-Oriented Programming': ['oop', 'object oriented'],
            'Data Structures': ['data structures', 'algorithms'],
            'Computer Networks': ['networks', 'networking', 'tcp/ip'],
            'Operating Systems': ['operating systems', 'os', 'linux'],
            'Cybersecurity': ['cybersecurity', 'security', 'cyber security'],
            'Artificial Intelligence': ['artificial intelligence', 'ai', 'intelligent systems'],
            'Deep Learning': ['deep learning', 'neural networks', 'cnn'],
            'Natural Language Processing': ['nlp', 'natural language processing'],
            'Computer Vision': ['computer vision', 'image processing'],
            'Big Data': ['big data', 'hadoop', 'spark'],
            'Data Mining': ['data mining', 'pattern recognition'],
            'Business Intelligence': ['business intelligence', 'bi', 'analytics'],
            'Project Management': ['project management', 'agile', 'scrum']
        }
        
        for skill, keywords in skill_keywords.items():
            for keyword in keywords:
                if keyword in full_text:
                    skills.append(skill)
                    break  # Avoid duplicate skills
        
        return list(set(skills))  # Remove duplicates
    
    def _analyze_course_offerings(self, course_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze course offerings"""
        
        if not course_data:
            return {'error': 'No course data available'}
        
        # Extract all skills
        all_skills = []
        departments = []
        levels = []
        
        for course in course_data:
            all_skills.extend(course.get('skills', []))
            departments.append(course['course_code'].split()[0] if ' ' in course['course_code'] else course['course_code'][:2])
            levels.append(course['level'])
        
        # Analyze skill frequency
        skill_frequency = {}
        for skill in all_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        top_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Analyze departments
        dept_frequency = {}
        for dept in departments:
            dept_frequency[dept] = dept_frequency.get(dept, 0) + 1
        
        # Analyze levels
        level_frequency = {}
        for level in levels:
            level_frequency[level] = level_frequency.get(level, 0) + 1
        
        return {
            'total_courses': len(course_data),
            'top_skills': top_skills,
            'departments': dept_frequency,
            'levels': level_frequency,
            'skill_frequency': skill_frequency
        }
    
    def _generate_course_recommendations(self, analysis: Dict[str, Any], query: str) -> str:
        """Generate course recommendations based on analysis"""
        
        if 'error' in analysis:
            return f"Unable to analyze course catalog: {analysis['error']}"
        
        recommendations = f"""
        **UTD Course Catalog Analysis for: {query}**
        
        **Course Overview:**
        - Total relevant courses found: {analysis['total_courses']}
        - Departments offering courses: {len(analysis['departments'])}
        - Course levels: {', '.join(analysis['levels'].keys())}
        
        **Top Skills Covered:**
        """
        
        for i, (skill, count) in enumerate(analysis['top_skills'][:8], 1):
            recommendations += f"{i}. {skill} (covered in {count} courses)\n"
        
        recommendations += f"""
        
        **Department Breakdown:**
        """
        
        for dept, count in sorted(analysis['departments'].items(), key=lambda x: x[1], reverse=True)[:5]:
            recommendations += f"- {dept}: {count} courses\n"
        
        recommendations += f"""
        
        **Key Insights:**
        - UTD offers comprehensive coverage of {query} related skills
        - Top departments: {', '.join([dept for dept, _ in sorted(analysis['departments'].items(), key=lambda x: x[1], reverse=True)[:3]])}
        - Most covered skills: {', '.join([skill for skill, _ in analysis['top_skills'][:3]])}
        
        **Recommendations:**
        - Focus on courses that cover the top 3 skills identified
        - Consider prerequisites when planning your course sequence
        - Look for courses in the most active departments
        - Balance between undergraduate and graduate level courses
        """
        
        return recommendations
