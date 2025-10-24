"""
AWS Lambda function for ProjectAdvisorAgent with real project scraping
Scrapes projects from Kaggle, GitHub, and other real sources
"""

import json
import boto3
from typing import Dict, Any, List
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import random

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for ProjectAdvisorAgent with real project scraping
    """
    
    try:
        # Extract query from event
        query = event.get('query', '')
        session_id = event.get('sessionId', '')
        
        print(f"Real ProjectAdvisorAgent processing query: {query}")
        
        # Initialize agent
        agent = RealProjectAdvisorAgent()
        
        # Process the query autonomously
        result = agent.process_project_advice_query(query)
        
        return {
            'statusCode': 200,
            'body': {
                'agent': 'RealProjectAdvisorAgent',
                'query': query,
                'result': result,
                'sessionId': session_id,
                'timestamp': datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"Error in RealProjectAdvisorAgent: {e}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'agent': 'RealProjectAdvisorAgent'
            }
        }

class RealProjectAdvisorAgent:
    """Real Project Advisor Agent that scrapes actual projects from Kaggle, GitHub, etc."""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'utd-career-guidance-data'
        
    def process_project_advice_query(self, query: str) -> Dict[str, Any]:
        """Process project advice query with real project scraping"""
        
        # Extract career keywords from query
        career_keywords = self._extract_career_keywords(query)
        
        # Scrape real projects from multiple sources
        kaggle_projects = self._scrape_kaggle_projects(career_keywords)
        github_projects = self._scrape_github_projects(career_keywords)
        medium_projects = self._scrape_medium_projects(career_keywords)
        
        # Combine all projects
        all_projects = kaggle_projects + github_projects + medium_projects
        
        # Rank projects by relevance
        ranked_projects = self._rank_projects_by_relevance(all_projects, career_keywords)
        
        # Generate project recommendations
        recommendations = self._generate_project_recommendations(ranked_projects, career_keywords)
        
        return {
            'career_keywords': career_keywords,
            'total_projects_found': len(all_projects),
            'kaggle_projects': len(kaggle_projects),
            'github_projects': len(github_projects),
            'medium_projects': len(medium_projects),
            'top_projects': ranked_projects[:5],
            'recommendations': recommendations,
            'scraping_timestamp': datetime.now().isoformat()
        }
    
    def _extract_career_keywords(self, query: str) -> List[str]:
        """Extract career-related keywords from query"""
        keywords = []
        
        # Common career terms
        career_terms = [
            'data scientist', 'data analyst', 'data engineer', 'machine learning engineer',
            'software engineer', 'web developer', 'business analyst', 'product manager',
            'python', 'sql', 'machine learning', 'deep learning', 'statistics',
            'data visualization', 'big data', 'cloud computing', 'aws', 'azure'
        ]
        
        query_lower = query.lower()
        for term in career_terms:
            if term in query_lower:
                keywords.append(term)
        
        return keywords if keywords else ['data scientist', 'python', 'machine learning']
    
    def _scrape_kaggle_projects(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Scrape real projects from Kaggle"""
        projects = []
        
        try:
            # Kaggle datasets and competitions
            kaggle_urls = [
                "https://www.kaggle.com/datasets",
                "https://www.kaggle.com/competitions"
            ]
            
            for url in kaggle_urls:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find project cards
                        project_cards = soup.find_all('div', class_='sc-fqkvVR')
                        
                        for card in project_cards[:5]:  # Limit to 5 projects
                            try:
                                title_elem = card.find('h3')
                                description_elem = card.find('p')
                                tags_elem = card.find('div', class_='sc-fqkvVR')
                                
                                if title_elem:
                                    project = {
                                        'title': title_elem.get_text(strip=True),
                                        'description': description_elem.get_text(strip=True) if description_elem else '',
                                        'source': 'Kaggle',
                                        'url': f"https://www.kaggle.com{card.find('a')['href']}" if card.find('a') else '',
                                        'type': 'Dataset' if 'datasets' in url else 'Competition',
                                        'tags': [tag.get_text(strip=True) for tag in tags_elem.find_all('span')] if tags_elem else [],
                                        'difficulty': 'Intermediate',
                                        'skills_developed': self._extract_skills_from_project(title_elem.get_text(strip=True)),
                                        'relevance_score': 0
                                    }
                                    projects.append(project)
                            except Exception as e:
                                continue
                                
                except Exception as e:
                    print(f"Error scraping Kaggle: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in Kaggle scraping: {e}")
        
        return projects
    
    def _scrape_github_projects(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Scrape real projects from GitHub"""
        projects = []
        
        try:
            # GitHub trending repositories
            github_urls = [
                "https://github.com/trending/python",
                "https://github.com/trending/machine-learning",
                "https://github.com/trending/data-science"
            ]
            
            for url in github_urls:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find repository cards
                        repo_cards = soup.find_all('article', class_='Box-row')
                        
                        for card in repo_cards[:5]:  # Limit to 5 projects
                            try:
                                title_elem = card.find('h2', class_='h3')
                                description_elem = card.find('p', class_='col-9')
                                language_elem = card.find('span', class_='d-inline-block')
                                stars_elem = card.find('a', class_='Link--muted')
                                
                                if title_elem:
                                    project = {
                                        'title': title_elem.get_text(strip=True),
                                        'description': description_elem.get_text(strip=True) if description_elem else '',
                                        'source': 'GitHub',
                                        'url': f"https://github.com{title_elem.find('a')['href']}" if title_elem.find('a') else '',
                                        'type': 'Open Source Project',
                                        'language': language_elem.get_text(strip=True) if language_elem else 'Python',
                                        'stars': stars_elem.get_text(strip=True) if stars_elem else '0',
                                        'difficulty': 'Advanced',
                                        'skills_developed': self._extract_skills_from_project(title_elem.get_text(strip=True)),
                                        'relevance_score': 0
                                    }
                                    projects.append(project)
                            except Exception as e:
                                continue
                                
                except Exception as e:
                    print(f"Error scraping GitHub: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in GitHub scraping: {e}")
        
        return projects
    
    def _scrape_medium_projects(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Scrape real projects from Medium articles"""
        projects = []
        
        try:
            # Medium data science articles
            medium_urls = [
                "https://medium.com/tag/data-science",
                "https://medium.com/tag/machine-learning",
                "https://medium.com/tag/python"
            ]
            
            for url in medium_urls:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find article cards
                        article_cards = soup.find_all('div', class_='postArticle')
                        
                        for card in article_cards[:3]:  # Limit to 3 projects
                            try:
                                title_elem = card.find('h3')
                                description_elem = card.find('p')
                                author_elem = card.find('span', class_='author')
                                
                                if title_elem:
                                    project = {
                                        'title': title_elem.get_text(strip=True),
                                        'description': description_elem.get_text(strip=True) if description_elem else '',
                                        'source': 'Medium',
                                        'url': card.find('a')['href'] if card.find('a') else '',
                                        'type': 'Tutorial/Article',
                                        'author': author_elem.get_text(strip=True) if author_elem else 'Unknown',
                                        'difficulty': 'Beginner',
                                        'skills_developed': self._extract_skills_from_project(title_elem.get_text(strip=True)),
                                        'relevance_score': 0
                                    }
                                    projects.append(project)
                            except Exception as e:
                                continue
                                
                except Exception as e:
                    print(f"Error scraping Medium: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in Medium scraping: {e}")
        
        return projects
    
    def _extract_skills_from_project(self, project_title: str) -> List[str]:
        """Extract skills from project title"""
        skills = []
        title_lower = project_title.lower()
        
        skill_keywords = {
            'Python': ['python', 'django', 'flask', 'pandas', 'numpy', 'scikit'],
            'Machine Learning': ['ml', 'machine learning', 'tensorflow', 'pytorch', 'scikit', 'neural'],
            'Data Science': ['data science', 'data analysis', 'visualization', 'statistics'],
            'Web Development': ['web', 'html', 'css', 'javascript', 'react', 'django', 'flask'],
            'Database': ['sql', 'database', 'mysql', 'postgresql', 'mongodb'],
            'Cloud': ['aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes'],
            'Statistics': ['statistics', 'statistical', 'regression', 'classification', 'clustering'],
            'Deep Learning': ['deep learning', 'neural network', 'cnn', 'rnn', 'lstm'],
            'Big Data': ['big data', 'spark', 'hadoop', 'kafka', 'streaming']
        }
        
        for skill, keywords in skill_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                skills.append(skill)
        
        return skills
    
    def _rank_projects_by_relevance(self, projects: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """Rank projects by relevance to keywords"""
        
        for project in projects:
            relevance_score = 0
            
            # Score based on keywords
            project_skills = project.get('skills_developed', [])
            for keyword in keywords:
                if keyword.lower() in ' '.join(project_skills).lower():
                    relevance_score += 2
                if keyword.lower() in project.get('title', '').lower():
                    relevance_score += 3
                if keyword.lower() in project.get('description', '').lower():
                    relevance_score += 1
            
            # Score based on source popularity
            if project.get('source') == 'GitHub' and project.get('stars', '0').isdigit():
                stars = int(project.get('stars', '0'))
                if stars > 1000:
                    relevance_score += 3
                elif stars > 100:
                    relevance_score += 2
                elif stars > 10:
                    relevance_score += 1
            
            # Score based on project type
            if project.get('type') == 'Competition':
                relevance_score += 2
            elif project.get('type') == 'Open Source Project':
                relevance_score += 1
            
            project['relevance_score'] = relevance_score
        
        # Sort by relevance score
        return sorted(projects, key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    def _generate_project_recommendations(self, ranked_projects: List[Dict[str, Any]], keywords: List[str]) -> str:
        """Generate project recommendations based on ranked projects"""
        
        if not ranked_projects:
            return "No projects found. Please try different keywords."
        
        recommendations = f"""
        **Real Project Recommendations for: {', '.join(keywords)}**
        
        **Top {min(3, len(ranked_projects))} Projects:**
        """
        
        for i, project in enumerate(ranked_projects[:3], 1):
            recommendations += f"""
        {i}. **{project['title']}**
           - Source: {project['source']}
           - Type: {project['type']}
           - Skills: {', '.join(project['skills_developed'])}
           - Difficulty: {project['difficulty']}
           - URL: {project['url']}
           - Description: {project['description'][:100]}...
        """
        
        recommendations += f"""
        
        **Key Insights:**
        - Found {len(ranked_projects)} relevant projects
        - Top sources: {', '.join(set(p['source'] for p in ranked_projects[:5]))}
        - Most common skills: {', '.join(set(skill for p in ranked_projects[:5] for skill in p['skills_developed']))}
        
        **Next Steps:**
        - Start with the highest-ranked project
        - Focus on developing the most common skills
        - Build a portfolio with diverse project types
        """
        
        return recommendations

if __name__ == "__main__":
    # Test the agent
    test_event = {
        'query': 'I want to become a data scientist',
        'sessionId': 'test123'
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
