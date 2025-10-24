"""
Career Guidance System - Multi-Agent Coordination Controller
Orchestrates all agents and provides unified career guidance responses
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
from dataclasses import dataclass

try:
    from agents import (
        JobMarketAgent,
        CourseCatalogAgent, 
        CareerMatchingAgent,
        ProjectAdvisorAgent
    )
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports
    from agents.job_market_agent import JobMarketAgent
    from agents.course_catalog_agent import CourseCatalogAgent
    from agents.career_matching_agent import CareerMatchingAgent
    from agents.project_advisor_agent import ProjectAdvisorAgent


@dataclass
class CareerGuidanceResponse:
    """Response structure for career guidance system."""
    user_query: str
    job_market_insights: str
    course_recommendations: str
    career_matching_analysis: str
    project_suggestions: str
    unified_response: str
    timestamp: str
    session_id: str


class CareerGuidanceSystem:
    """
    Main controller class that coordinates all career guidance agents
    and provides unified responses to user queries.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("CareerGuidanceSystem")
        self._setup_logging()
        
        # Initialize all agents
        self.job_market_agent = JobMarketAgent()
        self.course_catalog_agent = CourseCatalogAgent()
        self.career_matching_agent = CareerMatchingAgent()
        self.project_advisor_agent = ProjectAdvisorAgent()
        
        # System configuration
        self.config = {
            'max_concurrent_agents': 4,
            'response_timeout': 300,  # 5 minutes
            'enable_caching': True,
            'cache_duration': 3600  # 1 hour
        }
        
        # Session management
        self.active_sessions = {}
        
        # Create necessary directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('cache', exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration for the system."""
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/career_guidance_system.log')
            ]
        )
    
    async def process_query(self, user_query: str, session_id: str = None) -> CareerGuidanceResponse:
        """
        Process a user query through all agents and return unified response.
        
        Args:
            user_query: User's career guidance question
            session_id: Optional session identifier for caching
            
        Returns:
            Comprehensive career guidance response
        """
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.logger.info(f"Processing query for session {session_id}: {user_query[:100]}...")
        
        try:
            # Check cache first
            if self.config['enable_caching']:
                cached_response = self._get_cached_response(user_query, session_id)
                if cached_response:
                    self.logger.info(f"Returning cached response for session {session_id}")
                    return cached_response
            
            # Run all agents concurrently
            agent_responses = await self._run_agents_concurrently(user_query)
            
            # Generate unified response
            unified_response = await self._generate_unified_response(
                user_query, agent_responses
            )
            
            # Create response object
            response = CareerGuidanceResponse(
                user_query=user_query,
                job_market_insights=agent_responses.get('job_market', 'No job market insights available'),
                course_recommendations=agent_responses.get('course_catalog', 'No course recommendations available'),
                career_matching_analysis=agent_responses.get('career_matching', 'No career matching analysis available'),
                project_suggestions=agent_responses.get('project_advisor', 'No project suggestions available'),
                unified_response=unified_response,
                timestamp=datetime.now().isoformat(),
                session_id=session_id
            )
            
            # Cache the response
            if self.config['enable_caching']:
                self._cache_response(user_query, session_id, response)
            
            # Store session data
            self.active_sessions[session_id] = {
                'query': user_query,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Successfully processed query for session {session_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing query for session {session_id}: {e}")
            return self._create_error_response(user_query, session_id, str(e))
    
    async def _run_agents_concurrently(self, user_query: str) -> Dict[str, str]:
        """
        Run all agents concurrently to gather insights.
        
        Args:
            user_query: User's query
            
        Returns:
            Dictionary of agent responses
        """
        self.logger.info("Running all agents concurrently")
        
        # Create tasks for each agent
        tasks = {
            'job_market': self._run_job_market_agent(user_query),
            'course_catalog': self._run_course_catalog_agent(user_query),
            'career_matching': self._run_career_matching_agent(user_query),
            'project_advisor': self._run_project_advisor_agent(user_query)
        }
        
        # Execute all tasks concurrently with timeout
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks.values(), return_exceptions=True),
                timeout=self.config['response_timeout']
            )
            
            # Process results
            agent_responses = {}
            for i, (agent_name, result) in enumerate(zip(tasks.keys(), results)):
                if isinstance(result, Exception):
                    self.logger.error(f"Agent {agent_name} failed: {result}")
                    agent_responses[agent_name] = f"Error: {agent_name} agent failed - {str(result)}"
                else:
                    agent_responses[agent_name] = result
            
            return agent_responses
            
        except asyncio.TimeoutError:
            self.logger.error("Agent execution timed out")
            return {
                'job_market': 'Error: Job market analysis timed out',
                'course_catalog': 'Error: Course catalog analysis timed out',
                'career_matching': 'Error: Career matching analysis timed out',
                'project_advisor': 'Error: Project advisor analysis timed out'
            }
    
    async def _run_job_market_agent(self, user_query: str) -> str:
        """Run job market agent."""
        try:
            return await self.job_market_agent.run(user_query)
        except Exception as e:
            self.logger.error(f"Job market agent error: {e}")
            return f"Job market analysis unavailable: {str(e)}"
    
    async def _run_course_catalog_agent(self, user_query: str) -> str:
        """Run course catalog agent."""
        try:
            return await self.course_catalog_agent.run(user_query)
        except Exception as e:
            self.logger.error(f"Course catalog agent error: {e}")
            return f"Course catalog analysis unavailable: {str(e)}"
    
    async def _run_career_matching_agent(self, user_query: str) -> str:
        """Run career matching agent."""
        try:
            return await self.career_matching_agent.run(user_query)
        except Exception as e:
            self.logger.error(f"Career matching agent error: {e}")
            return f"Career matching analysis unavailable: {str(e)}"
    
    async def _run_project_advisor_agent(self, user_query: str) -> str:
        """Run project advisor agent."""
        try:
            return await self.project_advisor_agent.run(user_query)
        except Exception as e:
            self.logger.error(f"Project advisor agent error: {e}")
            return f"Project advisor analysis unavailable: {str(e)}"
    
    async def _generate_unified_response(self, user_query: str, 
                                       agent_responses: Dict[str, str]) -> str:
        """
        Generate a unified response combining all agent insights.
        
        Args:
            user_query: Original user query
            agent_responses: Responses from all agents
            
        Returns:
            Unified response string
        """
        self.logger.info("Generating unified response")
        
        # Create a comprehensive prompt for unified response
        prompt = f"""
        As a comprehensive career guidance AI system, synthesize the following information to provide a unified, actionable response to the user's query.

        **User Query:** {user_query}

        **Job Market Insights:**
        {agent_responses.get('job_market', 'No job market data available')}

        **Course Recommendations:**
        {agent_responses.get('course_catalog', 'No course data available')}

        **Career Matching Analysis:**
        {agent_responses.get('career_matching', 'No career matching data available')}

        **Project Suggestions:**
        {agent_responses.get('project_advisor', 'No project data available')}

        Please provide a comprehensive, unified response that:
        1. Directly addresses the user's query
        2. Integrates insights from all four analysis areas
        3. Provides clear, actionable next steps
        4. Prioritizes recommendations based on market demand and skill gaps
        5. Includes specific courses and projects to pursue
        6. Offers a realistic timeline for career development
        7. Maintains a supportive and encouraging tone

        Structure your response with clear sections and bullet points for easy reading.
        """
        
        # Use the job market agent's Bedrock client for unified response
        try:
            unified_response = await self.job_market_agent.invoke_bedrock(prompt)
            return unified_response
        except Exception as e:
            self.logger.error(f"Error generating unified response: {e}")
            return self._create_fallback_response(user_query, agent_responses)
    
    def _create_fallback_response(self, user_query: str, 
                                agent_responses: Dict[str, str]) -> str:
        """Create a fallback response if Bedrock fails."""
        return f"""
        Based on your query: "{user_query}"

        Here's a comprehensive career guidance summary:

        **Job Market Insights:**
        {agent_responses.get('job_market', 'No job market data available')}

        **Course Recommendations:**
        {agent_responses.get('course_catalog', 'No course data available')}

        **Career Matching Analysis:**
        {agent_responses.get('career_matching', 'No career matching data available')}

        **Project Suggestions:**
        {agent_responses.get('project_advisor', 'No project data available')}

        **Next Steps:**
        1. Review the job market insights to understand current demand
        2. Identify relevant courses from the recommendations
        3. Focus on skills with high market demand
        4. Start with the suggested projects to build practical experience
        5. Create a timeline for your career development journey

        For more detailed guidance, please refine your query or ask specific questions about any of these areas.
        """
    
    def _create_error_response(self, user_query: str, session_id: str, 
                             error_message: str) -> CareerGuidanceResponse:
        """Create an error response when processing fails."""
        return CareerGuidanceResponse(
            user_query=user_query,
            job_market_insights="Error: Unable to fetch job market data",
            course_recommendations="Error: Unable to fetch course data",
            career_matching_analysis="Error: Unable to perform career matching",
            project_suggestions="Error: Unable to generate project suggestions",
            unified_response=f"I apologize, but I encountered an error while processing your query: {error_message}. Please try again or contact support if the issue persists.",
            timestamp=datetime.now().isoformat(),
            session_id=session_id
        )
    
    def _get_cached_response(self, user_query: str, session_id: str) -> Optional[CareerGuidanceResponse]:
        """Get cached response if available."""
        try:
            cache_file = f"cache/response_{session_id}.json"
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                    return CareerGuidanceResponse(**cached_data)
        except Exception as e:
            self.logger.warning(f"Error reading cache: {e}")
        return None
    
    def _cache_response(self, user_query: str, session_id: str, 
                       response: CareerGuidanceResponse):
        """Cache the response for future use."""
        try:
            cache_file = f"cache/response_{session_id}.json"
            with open(cache_file, 'w') as f:
                json.dump(response.__dict__, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Error caching response: {e}")
    
    def get_session_history(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session history for a given session ID."""
        return self.active_sessions.get(session_id)
    
    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all active sessions."""
        return self.active_sessions.copy()
    
    def clear_session(self, session_id: str) -> bool:
        """Clear a specific session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            # Also remove cache file
            cache_file = f"cache/response_{session_id}.json"
            if os.path.exists(cache_file):
                os.remove(cache_file)
            return True
        return False
    
    def clear_all_sessions(self):
        """Clear all sessions and cache."""
        self.active_sessions.clear()
        # Clear cache directory
        import shutil
        if os.path.exists('cache'):
            shutil.rmtree('cache')
        os.makedirs('cache', exist_ok=True)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and health information."""
        return {
            'status': 'operational',
            'active_sessions': len(self.active_sessions),
            'agents_initialized': True,
            'cache_enabled': self.config['enable_caching'],
            'max_concurrent_agents': self.config['max_concurrent_agents'],
            'response_timeout': self.config['response_timeout'],
            'timestamp': datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on all agents."""
        health_status = {
            'overall_status': 'healthy',
            'agents': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Test each agent
        agents = {
            'job_market': self.job_market_agent,
            'course_catalog': self.course_catalog_agent,
            'career_matching': self.career_matching_agent,
            'project_advisor': self.project_advisor_agent
        }
        
        for agent_name, agent in agents.items():
            try:
                # Simple test to see if agent can be instantiated and basic methods exist
                health_status['agents'][agent_name] = {
                    'status': 'healthy',
                    'bedrock_client_available': agent.bedrock_client is not None,
                    'logger_configured': agent.logger is not None
                }
            except Exception as e:
                health_status['agents'][agent_name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['overall_status'] = 'degraded'
        
        return health_status


# AWS Lambda compatibility
async def lambda_handler(event, context):
    """
    AWS Lambda handler for the career guidance system.
    
    Args:
        event: Lambda event object
        context: Lambda context object
        
    Returns:
        Lambda response object
    """
    try:
        # Extract query from event
        user_query = event.get('query', '')
        session_id = event.get('sessionId', f"lambda_{context.aws_request_id}")
        
        if not user_query:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No query provided',
                    'message': 'Please provide a query in the event body'
                })
            }
        
        # Initialize system
        system = CareerGuidanceSystem()
        
        # Process query
        response = await system.process_query(user_query, session_id)
        
        # Return response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'query': response.user_query,
                'unified_response': response.unified_response,
                'job_market_insights': response.job_market_insights,
                'course_recommendations': response.course_recommendations,
                'career_matching_analysis': response.career_matching_analysis,
                'project_suggestions': response.project_suggestions,
                'session_id': response.session_id,
                'timestamp': response.timestamp
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


# Main execution for testing
async def main():
    """Main function for testing the career guidance system."""
    system = CareerGuidanceSystem()
    
    # Test queries
    test_queries = [
        "I want to become a data scientist. What should I learn?",
        "What are the most in-demand skills in tech right now?",
        "I'm a beginner in programming. What projects should I start with?",
        "What courses should I take to transition into machine learning?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        response = await system.process_query(query)
        
        print(f"Unified Response:\n{response.unified_response}")
        print(f"\nSession ID: {response.session_id}")
        print(f"Timestamp: {response.timestamp}")


if __name__ == "__main__":
    asyncio.run(main())
