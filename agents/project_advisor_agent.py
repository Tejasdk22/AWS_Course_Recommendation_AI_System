"""
Project Advisor Agent for AWS Course Recommendation AI System
Analyzes skill gaps and suggests hands-on projects for career development
"""

import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
try:
    from .base_agent import BaseAgent
except ImportError:
    from base_agent import BaseAgent


class ProjectAdvisorAgent(BaseAgent):
    """
    Agent responsible for analyzing skill gaps and suggesting
    hands-on projects for career development.
    """
    
    def __init__(self):
        super().__init__("ProjectAdvisorAgent")
        self.github_api_base = "https://api.github.com"
        self.project_categories = {
            'data_science': {
                'keywords': ['data science', 'machine learning', 'data analysis', 'python', 'jupyter'],
                'difficulty_levels': ['beginner', 'intermediate', 'advanced']
            },
            'web_development': {
                'keywords': ['web development', 'react', 'javascript', 'html', 'css', 'node'],
                'difficulty_levels': ['beginner', 'intermediate', 'advanced']
            },
            'mobile_development': {
                'keywords': ['mobile', 'ios', 'android', 'react native', 'flutter'],
                'difficulty_levels': ['beginner', 'intermediate', 'advanced']
            },
            'devops': {
                'keywords': ['devops', 'docker', 'kubernetes', 'aws', 'ci/cd'],
                'difficulty_levels': ['intermediate', 'advanced']
            }
        }
        self.sample_projects = self._load_sample_projects()
    
    def _load_sample_projects(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load sample projects for different categories and skill levels."""
        return {
            'data_science': {
                'beginner': [
                    {
                        'title': 'Exploratory Data Analysis (EDA) Project',
                        'description': 'Analyze a dataset of your choice using Python and create visualizations',
                        'skills': ['Python', 'Pandas', 'Matplotlib', 'Seaborn', 'Data Analysis'],
                        'tools': ['Jupyter Notebook', 'Python', 'Pandas', 'Matplotlib', 'Seaborn'],
                        'duration': '2-3 weeks',
                        'difficulty': 'Beginner',
                        'github_url': 'https://github.com/example/eda-project',
                        'learning_outcomes': [
                            'Data cleaning and preprocessing',
                            'Statistical analysis and visualization',
                            'Data storytelling with charts'
                        ]
                    },
                    {
                        'title': 'Predictive Modeling with Scikit-learn',
                        'description': 'Build a machine learning model to predict outcomes using real-world data',
                        'skills': ['Python', 'Scikit-learn', 'Machine Learning', 'Statistics'],
                        'tools': ['Jupyter Notebook', 'Python', 'Scikit-learn', 'Pandas'],
                        'duration': '3-4 weeks',
                        'difficulty': 'Beginner',
                        'github_url': 'https://github.com/example/ml-prediction',
                        'learning_outcomes': [
                            'Model training and evaluation',
                            'Feature engineering',
                            'Cross-validation techniques'
                        ]
                    }
                ],
                'intermediate': [
                    {
                        'title': 'End-to-End Data Science Pipeline',
                        'description': 'Create a complete data science project from data collection to deployment',
                        'skills': ['Python', 'Machine Learning', 'Docker', 'Flask', 'AWS'],
                        'tools': ['Python', 'Docker', 'Flask', 'AWS S3', 'PostgreSQL'],
                        'duration': '6-8 weeks',
                        'difficulty': 'Intermediate',
                        'github_url': 'https://github.com/example/end-to-end-ds',
                        'learning_outcomes': [
                            'Full-stack data science development',
                            'Model deployment and monitoring',
                            'Cloud computing and containerization'
                        ]
                    },
                    {
                        'title': 'Deep Learning Image Classification',
                        'description': 'Build a CNN model for image classification using TensorFlow/PyTorch',
                        'skills': ['Python', 'TensorFlow', 'Deep Learning', 'Computer Vision'],
                        'tools': ['Python', 'TensorFlow', 'OpenCV', 'Jupyter Notebook'],
                        'duration': '4-6 weeks',
                        'difficulty': 'Intermediate',
                        'github_url': 'https://github.com/example/cnn-classification',
                        'learning_outcomes': [
                            'Deep learning fundamentals',
                            'Computer vision techniques',
                            'Model optimization and tuning'
                        ]
                    }
                ],
                'advanced': [
                    {
                        'title': 'Real-time Recommendation System',
                        'description': 'Build a scalable recommendation system using Apache Spark and Kafka',
                        'skills': ['Python', 'Apache Spark', 'Kafka', 'Machine Learning', 'Big Data'],
                        'tools': ['Python', 'Apache Spark', 'Kafka', 'Redis', 'Docker'],
                        'duration': '8-12 weeks',
                        'difficulty': 'Advanced',
                        'github_url': 'https://github.com/example/recommendation-system',
                        'learning_outcomes': [
                            'Big data processing',
                            'Real-time streaming',
                            'Distributed computing'
                        ]
                    }
                ]
            },
            'web_development': {
                'beginner': [
                    {
                        'title': 'Personal Portfolio Website',
                        'description': 'Create a responsive portfolio website using HTML, CSS, and JavaScript',
                        'skills': ['HTML', 'CSS', 'JavaScript', 'Responsive Design'],
                        'tools': ['VS Code', 'Git', 'GitHub Pages'],
                        'duration': '2-3 weeks',
                        'difficulty': 'Beginner',
                        'github_url': 'https://github.com/example/portfolio-website',
                        'learning_outcomes': [
                            'Frontend development basics',
                            'Responsive web design',
                            'Version control with Git'
                        ]
                    }
                ],
                'intermediate': [
                    {
                        'title': 'Full-Stack E-commerce Application',
                        'description': 'Build a complete e-commerce platform with React frontend and Node.js backend',
                        'skills': ['React', 'Node.js', 'MongoDB', 'Express', 'JWT'],
                        'tools': ['React', 'Node.js', 'MongoDB', 'Postman', 'Docker'],
                        'duration': '6-8 weeks',
                        'difficulty': 'Intermediate',
                        'github_url': 'https://github.com/example/ecommerce-app',
                        'learning_outcomes': [
                            'Full-stack development',
                            'Database design and management',
                            'Authentication and security'
                        ]
                    }
                ]
            }
        }
    
    async def fetch_data(self) -> Dict[str, Any]:
        """
        Fetch project data from GitHub and other sources.
        
        Returns:
            Project data including GitHub repositories and sample projects
        """
        self.logger.info("Fetching project data for career guidance")
        
        # Load career matching data to understand skill gaps
        career_matching_data = self.load_data('career_matching_analysis.json')
        
        # Fetch GitHub projects (simulated for now)
        github_projects = await self._fetch_github_projects()
        
        # Combine with sample projects
        all_projects = {
            'github_projects': github_projects,
            'sample_projects': self.sample_projects,
            'career_matching_data': career_matching_data,
            'fetched_at': datetime.now().isoformat()
        }
        
        return all_projects
    
    async def _fetch_github_projects(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch relevant projects from GitHub (simulated for now)."""
        # In a real implementation, this would use GitHub API
        # For now, return sample data
        return {
            'trending_data_science': [
                {
                    'name': 'awesome-machine-learning',
                    'description': 'A curated list of machine learning frameworks, libraries and software',
                    'stars': 58000,
                    'language': 'Python',
                    'url': 'https://github.com/josephmisiti/awesome-machine-learning',
                    'topics': ['machine-learning', 'data-science', 'python']
                }
            ],
            'trending_web_development': [
                {
                    'name': 'freeCodeCamp',
                    'description': 'freeCodeCamp.org\'s open source codebase and curriculum',
                    'stars': 370000,
                    'language': 'JavaScript',
                    'url': 'https://github.com/freeCodeCamp/freeCodeCamp',
                    'topics': ['javascript', 'education', 'web-development']
                }
            ]
        }
    
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process project data and create personalized project recommendations.
        
        Args:
            data: Raw project data
            
        Returns:
            Processed project recommendations
        """
        self.logger.info("Processing project advisor data")
        
        career_matching_data = data.get('career_matching_data', {})
        skill_gaps = career_matching_data.get('skill_gaps', {})
        recommendations = career_matching_data.get('recommendations', [])
        
        # Analyze skill gaps to determine project priorities
        project_priorities = self._analyze_skill_gaps_for_projects(skill_gaps, recommendations)
        
        # Generate personalized project recommendations
        personalized_projects = self._generate_personalized_projects(
            project_priorities, data.get('sample_projects', {})
        )
        
        # Create learning paths
        learning_paths = self._create_learning_paths(personalized_projects)
        
        # Generate project roadmaps
        project_roadmaps = self._create_project_roadmaps(personalized_projects)
        
        processed_data = {
            'project_priorities': project_priorities,
            'personalized_projects': personalized_projects,
            'learning_paths': learning_paths,
            'project_roadmaps': project_roadmaps,
            'total_projects_recommended': sum(len(projects) for projects in personalized_projects.values()),
            'processed_at': datetime.now().isoformat()
        }
        
        self.logger.info("Project advisor data processing completed")
        return processed_data
    
    def _analyze_skill_gaps_for_projects(self, skill_gaps: Dict[str, Any], 
                                       recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze skill gaps to determine project priorities."""
        priorities = {
            'high_priority_skills': [],
            'medium_priority_skills': [],
            'low_priority_skills': [],
            'skill_categories': {}
        }
        
        # Process high demand, low supply skills
        high_demand_skills = skill_gaps.get('high_demand_low_supply', [])
        for skill_info in high_demand_skills:
            skill = skill_info['skill']
            priorities['high_priority_skills'].append({
                'skill': skill,
                'demand': skill_info['job_frequency'],
                'supply': skill_info['course_frequency'],
                'priority': 'High'
            })
        
        # Process missing skills from courses
        missing_skills = skill_gaps.get('missing_from_courses', [])
        for skill_info in missing_skills:
            skill = skill_info['skill']
            priorities['high_priority_skills'].append({
                'skill': skill,
                'demand': skill_info['job_frequency'],
                'supply': 0,
                'priority': 'High'
            })
        
        # Categorize skills
        for skill_info in priorities['high_priority_skills']:
            skill = skill_info['skill']
            category = self._categorize_skill(skill)
            if category not in priorities['skill_categories']:
                priorities['skill_categories'][category] = []
            priorities['skill_categories'][category].append(skill_info)
        
        return priorities
    
    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill into project categories."""
        skill_lower = skill.lower()
        
        if any(keyword in skill_lower for keyword in ['python', 'machine learning', 'data', 'statistics', 'pandas', 'numpy']):
            return 'data_science'
        elif any(keyword in skill_lower for keyword in ['javascript', 'react', 'html', 'css', 'web', 'frontend', 'backend']):
            return 'web_development'
        elif any(keyword in skill_lower for keyword in ['mobile', 'ios', 'android', 'react native', 'flutter']):
            return 'mobile_development'
        elif any(keyword in skill_lower for keyword in ['aws', 'docker', 'kubernetes', 'devops', 'ci/cd']):
            return 'devops'
        else:
            return 'general'
    
    def _generate_personalized_projects(self, priorities: Dict[str, Any], 
                                      sample_projects: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate personalized project recommendations based on skill priorities."""
        personalized_projects = {}
        
        # Get high priority skill categories
        high_priority_categories = priorities.get('skill_categories', {})
        
        for category, skills in high_priority_categories.items():
            if category in sample_projects:
                # Select projects based on skill requirements
                category_projects = sample_projects[category]
                recommended_projects = []
                
                for difficulty, projects in category_projects.items():
                    for project in projects:
                        project_skills = project.get('skills', [])
                        skill_overlap = set(skill['skill'] for skill in skills) & set(project_skills)
                        
                        if skill_overlap:
                            # Add skill gap information to project
                            project_copy = project.copy()
                            project_copy['targeted_skills'] = list(skill_overlap)
                            project_copy['skill_gap_relevance'] = len(skill_overlap) / len(project_skills)
                            recommended_projects.append(project_copy)
                
                # Sort by relevance and limit to top 3 per category
                recommended_projects.sort(key=lambda x: x['skill_gap_relevance'], reverse=True)
                personalized_projects[category] = recommended_projects[:3]
        
        return personalized_projects
    
    def _create_learning_paths(self, personalized_projects: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Create structured learning paths based on project recommendations."""
        learning_paths = []
        
        for category, projects in personalized_projects.items():
            if not projects:
                continue
            
            # Sort projects by difficulty
            difficulty_order = ['beginner', 'intermediate', 'advanced']
            sorted_projects = sorted(projects, key=lambda x: difficulty_order.index(x.get('difficulty', 'beginner').lower()))
            
            learning_path = {
                'category': category.replace('_', ' ').title(),
                'total_projects': len(sorted_projects),
                'estimated_duration': self._calculate_total_duration(sorted_projects),
                'projects': sorted_projects,
                'prerequisites': self._extract_prerequisites(sorted_projects),
                'learning_outcomes': self._extract_learning_outcomes(sorted_projects)
            }
            
            learning_paths.append(learning_path)
        
        return learning_paths
    
    def _create_project_roadmaps(self, personalized_projects: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Create detailed project roadmaps with timelines."""
        roadmaps = []
        
        for category, projects in personalized_projects.items():
            if not projects:
                continue
            
            roadmap = {
                'category': category.replace('_', ' ').title(),
                'timeline': self._create_timeline(projects),
                'milestones': self._create_milestones(projects),
                'resources': self._gather_resources(projects),
                'success_metrics': self._define_success_metrics(projects)
            }
            
            roadmaps.append(roadmap)
        
        return roadmaps
    
    def _calculate_total_duration(self, projects: List[Dict[str, Any]]) -> str:
        """Calculate total duration for a list of projects."""
        total_weeks = 0
        for project in projects:
            duration = project.get('duration', '2-3 weeks')
            # Extract number from duration string
            weeks = re.findall(r'\d+', duration)
            if weeks:
                total_weeks += int(weeks[0])
        
        if total_weeks <= 12:
            return f"{total_weeks} weeks"
        else:
            months = total_weeks // 4
            return f"{months} months"
    
    def _extract_prerequisites(self, projects: List[Dict[str, Any]]) -> List[str]:
        """Extract prerequisites from projects."""
        prerequisites = set()
        for project in projects:
            skills = project.get('skills', [])
            prerequisites.update(skills)
        return list(prerequisites)
    
    def _extract_learning_outcomes(self, projects: List[Dict[str, Any]]) -> List[str]:
        """Extract learning outcomes from projects."""
        outcomes = set()
        for project in projects:
            project_outcomes = project.get('learning_outcomes', [])
            outcomes.update(project_outcomes)
        return list(outcomes)
    
    def _create_timeline(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create a timeline for project completion."""
        timeline = []
        current_week = 1
        
        for i, project in enumerate(projects):
            duration = project.get('duration', '2-3 weeks')
            weeks = re.findall(r'\d+', duration)
            project_weeks = int(weeks[0]) if weeks else 2
            
            timeline.append({
                'project': project['title'],
                'start_week': current_week,
                'end_week': current_week + project_weeks - 1,
                'duration': project_weeks,
                'difficulty': project.get('difficulty', 'Beginner')
            })
            
            current_week += project_weeks
        
        return timeline
    
    def _create_milestones(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create milestones for project completion."""
        milestones = []
        
        for i, project in enumerate(projects):
            milestones.append({
                'milestone': f"Complete {project['title']}",
                'project_index': i + 1,
                'description': project.get('description', ''),
                'success_criteria': [
                    f"Implement all required features",
                    f"Write clean, documented code",
                    f"Create a GitHub repository",
                    f"Write a comprehensive README"
                ]
            })
        
        return milestones
    
    def _gather_resources(self, projects: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Gather learning resources for projects."""
        resources = {
            'documentation': [],
            'tutorials': [],
            'tools': [],
            'communities': []
        }
        
        for project in projects:
            tools = project.get('tools', [])
            resources['tools'].extend(tools)
            
            # Add common resources based on skills
            skills = project.get('skills', [])
            for skill in skills:
                if 'python' in skill.lower():
                    resources['documentation'].append('Python Official Documentation')
                    resources['tutorials'].append('Python for Data Science - Coursera')
                elif 'react' in skill.lower():
                    resources['documentation'].append('React Official Documentation')
                    resources['tutorials'].append('React Tutorial - Official')
        
        # Remove duplicates
        for key in resources:
            resources[key] = list(set(resources[key]))
        
        return resources
    
    def _define_success_metrics(self, projects: List[Dict[str, Any]]) -> List[str]:
        """Define success metrics for project completion."""
        return [
            "All projects completed and deployed",
            "GitHub repositories with clean, documented code",
            "Portfolio showcasing completed projects",
            "Demonstrated understanding through project presentations",
            "Active participation in relevant communities"
        ]
    
    async def respond(self, processed_data: Dict[str, Any], user_query: str = None) -> str:
        """
        Generate a response based on processed project advisor data.
        
        Args:
            processed_data: Processed project advisor analysis
            user_query: Optional user query for context
            
        Returns:
            Generated response about project recommendations
        """
        if not processed_data:
            return "No project advisor data available to analyze."
        
        # Save processed data
        self.save_data(processed_data, 'project_advisor_analysis.json')
        
        # Generate response using Bedrock
        prompt = self._create_project_advisor_prompt(processed_data, user_query)
        response = await self.invoke_bedrock(prompt)
        
        return response
    
    def _create_project_advisor_prompt(self, data: Dict[str, Any], user_query: str = None) -> str:
        """Create a prompt for project advisor analysis."""
        
        personalized_projects = data.get('personalized_projects', {})
        learning_paths = data.get('learning_paths', [])
        project_roadmaps = data.get('project_roadmaps', [])
        
        prompt = f"""
        As a career guidance AI, analyze the following project recommendations:

        **Project Recommendations Overview:**
        - Total projects recommended: {data.get('total_projects_recommended', 0)}
        - Analysis date: {data.get('processed_at', 'N/A')}

        **Personalized Projects by Category:**
        {self._format_projects_by_category(personalized_projects)}

        **Learning Paths:**
        {self._format_learning_paths(learning_paths)}

        **Project Roadmaps:**
        {self._format_project_roadmaps(project_roadmaps)}

        **User Query:** {user_query or 'General project recommendations'}

        Please provide:
        1. Overview of recommended projects and their relevance to career goals
        2. Structured learning paths with clear progression
        3. Timeline and milestones for project completion
        4. Required tools and resources for each project
        5. Success metrics and evaluation criteria
        6. Tips for building a strong project portfolio

        Format your response in a clear, actionable manner suitable for career guidance.
        """
        
        return prompt
    
    def _format_projects_by_category(self, personalized_projects: Dict[str, List[Dict[str, Any]]]) -> str:
        """Format projects by category for display."""
        if not personalized_projects:
            return "No personalized projects available"
        
        formatted = []
        for category, projects in personalized_projects.items():
            if projects:
                formatted.append(f"\n**{category.replace('_', ' ').title()}:**")
                for i, project in enumerate(projects, 1):
                    formatted.append(
                        f"{i}. {project['title']} - {project.get('difficulty', 'Unknown')} "
                        f"({project.get('duration', 'Unknown duration')})"
                    )
        
        return "\n".join(formatted)
    
    def _format_learning_paths(self, learning_paths: List[Dict[str, Any]]) -> str:
        """Format learning paths for display."""
        if not learning_paths:
            return "No learning paths available"
        
        formatted = []
        for i, path in enumerate(learning_paths, 1):
            formatted.append(
                f"{i}. {path['category']} - {path['total_projects']} projects "
                f"({path['estimated_duration']})"
            )
        
        return "\n".join(formatted)
    
    def _format_project_roadmaps(self, project_roadmaps: List[Dict[str, Any]]) -> str:
        """Format project roadmaps for display."""
        if not project_roadmaps:
            return "No project roadmaps available"
        
        formatted = []
        for i, roadmap in enumerate(project_roadmaps, 1):
            formatted.append(f"{i}. {roadmap['category']} - {len(roadmap.get('timeline', []))} timeline items")
        
        return "\n".join(formatted)
