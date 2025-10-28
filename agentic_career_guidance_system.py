"""
Enhanced Agentic Career Guidance System
Implements dynamic orchestration, planning, and learning capabilities
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

try:
    from agents.agentic_base_agent import AgenticBaseAgent, AgenticPlan
    from agents.base_agent import BaseAgent
    from agents import (
        JobMarketAgent,
        CourseCatalogAgent,
        CareerMatchingAgent,
        ProjectAdvisorAgent
    )
except ImportError:
    from agents.agentic_base_agent import AgenticBaseAgent, AgenticPlan
    from agents.base_agent import BaseAgent
    from agents.job_market_agent import JobMarketAgent
    from agents.course_catalog_agent import CourseCatalogAgent
    from agents.career_matching_agent import CareerMatchingAgent
    from agents.project_advisor_agent import ProjectAdvisorAgent


@dataclass
class AgenticResponse:
    """Enhanced response with agentic capabilities"""
    user_query: str
    plan: Dict[str, Any]
    agent_execution: Dict[str, Any]
    unified_response: str
    context_used: str
    tools_selected: List[str]
    learning_insights: Dict[str, Any]
    timestamp: str
    session_id: str


class AgenticCareerGuidanceSystem:
    """
    Enhanced agentic orchestrator with:
    - Dynamic agent selection
    - Context-aware planning
    - Iterative refinement
    - Learning capabilities
    """
    
    def __init__(self):
        self.logger = logging.getLogger("AgenticCareerGuidanceSystem")
        self._setup_logging()
        
        # Initialize standard agents (can be enhanced with agentic capabilities)
        self.job_market_agent = JobMarketAgent()
        self.course_catalog_agent = CourseCatalogAgent()
        self.career_matching_agent = CareerMatchingAgent()
        self.project_advisor_agent = ProjectAdvisorAgent()
        
        # Agentic capabilities
        self.agent_registry = {
            'job_market': self.job_market_agent,
            'course_catalog': self.course_catalog_agent,
            'career_matching': self.career_matching_agent,
            'project_advisor': self.project_advisor_agent
        }
        
        self.session_context = {}
        self.learning_history = []
        
        # Create necessary directories
        import os
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('cache', exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        import os
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/agentic_career_guidance_system.log')
            ]
        )
    
    async def plan_query(self, user_query: str, context: Dict = None) -> Dict[str, Any]:
        """
        Use Bedrock to plan the execution strategy
        
        Args:
            user_query: User's query
            context: Optional context
            
        Returns:
            Execution plan
        """
        self.logger.info(f"Planning execution for: {user_query}")
        
        # Build planning prompt
        prompt = f"""
        As an intelligent agentic orchestrator, create an execution plan for this query:
        
        Query: {user_query}
        Available Agents: {list(self.agent_registry.keys())}
        Context: {context or 'No previous context'}
        
        Create a plan that:
        1. Identifies which agents are needed
        2. Determines the order of execution
        3. Defines dependencies between agents
        4. Specifies what information each agent needs
        5. Outlines expected outputs
        
        Return JSON with structure:
        {{
            "agents_to_use": ["agent1", "agent2", ...],
            "execution_order": ["agent1", "agent2", ...],
            "dependencies": {{"agent2": ["agent1"]}},
            "expected_outputs": {{"agent1": "description", ...}}
        }}
        """
        
        try:
            # Use job_market_agent's Bedrock client for planning
            plan_text = await self.job_market_agent.invoke_bedrock(prompt)
            
            # Parse plan
            plan = self._parse_execution_plan(plan_text)
            
            self.logger.info(f"Created plan with agents: {plan.get('agents_to_use', [])}")
            
            return plan
            
        except Exception as e:
            self.logger.error(f"Planning failed: {e}")
            # Fallback to using all agents
            return {
                "agents_to_use": list(self.agent_registry.keys()),
                "execution_order": list(self.agent_registry.keys()),
                "dependencies": {},
                "expected_outputs": {}
            }
    
    async def process_query(self, user_query: str, session_id: str = None, 
                          major: str = None, student_type: str = None) -> AgenticResponse:
        """
        Process query with agentic capabilities
        
        Args:
            user_query: User's query
            session_id: Session identifier
            major: User's major
            student_type: Student type (graduate/undergraduate)
            
        Returns:
            AgenticResponse with all details
        """
        # Create session
        if not session_id:
            session_id = f"agentic_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Retrieve context for this session
        context = self.session_context.get(session_id, {})
        
        # Step 1: Plan the execution
        execution_plan = await self.plan_query(user_query, context)
        
        # Step 2: Execute agents based on plan
        agent_results = {}
        execution_order = execution_plan.get('execution_order', list(self.agent_registry.keys()))
        
        for agent_name in execution_order:
            agent = self.agent_registry.get(agent_name)
            if not agent:
                continue
            
            # Check dependencies
            dependencies = execution_plan.get('dependencies', {}).get(agent_name, [])
            if dependencies:
                # Wait for dependencies
                for dep in dependencies:
                    if dep in agent_results:
                        context.update(agent_results[dep])
            
            # Execute agent
            self.logger.info(f"Executing agent: {agent_name}")
            
            try:
                if agent_name == 'course_catalog':
                    result = await agent.run(user_query, major=major, student_type=student_type)
                else:
                    result = await agent.run(user_query)
                
                agent_results[agent_name] = result
                
            except Exception as e:
                self.logger.error(f"Agent {agent_name} failed: {e}")
                agent_results[agent_name] = f"Error: {str(e)}"
        
        # Step 3: Generate unified response
        unified_response = await self._generate_unified_response(
            user_query,
            agent_results,
            execution_plan
        )
        
        # Step 4: Extract insights
        learning_insights = await self._extract_learning_insights(
            user_query,
            agent_results,
            unified_response
        )
        
        # Store in context for next interaction
        self.session_context[session_id] = {
            'query': user_query,
            'agents_used': execution_order,
            'results': agent_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Create response
        response = AgenticResponse(
            user_query=user_query,
            plan=execution_plan,
            agent_execution=agent_results,
            unified_response=unified_response,
            context_used=str(context),
            tools_selected=execution_order,
            learning_insights=learning_insights,
            timestamp=datetime.now().isoformat(),
            session_id=session_id
        )
        
        # Learn from this execution
        await self._learn_from_execution(response)
        
        return response
    
    async def _generate_unified_response(self, user_query: str, agent_results: Dict, plan: Dict) -> str:
        """Generate unified response using Bedrock"""
        prompt = f"""
        As an intelligent career guidance system, create a unified response.
        
        User Query: {user_query}
        
        Agent Results:
        {json.dumps(agent_results, indent=2)}
        
        Execution Plan:
        {json.dumps(plan, indent=2)}
        
        Create a comprehensive, coherent response that integrates all agent insights.
        Make it personalized, actionable, and specific to UTD courses and career paths.
        """
        
        try:
            unified = await self.job_market_agent.invoke_bedrock(prompt)
            return unified
        except Exception as e:
            self.logger.error(f"Unified response generation failed: {e}")
            return str(agent_results)
    
    async def _extract_learning_insights(self, query: str, results: Dict, unified: str) -> Dict:
        """Extract learning insights from execution"""
        prompt = f"""
        Extract key insights from this execution:
        
        Query: {query}
        Results: {json.dumps(results, indent=2)}
        
        Return JSON with:
        {{
            "effectiveness": "score 1-10",
            "agent_performance": {{"agent_name": "score"}},
            "key_learnings": ["learning1", "learning2", ...],
            "improvements_suggested": ["improvement1", ...]
        }}
        """
        
        try:
            insights_text = await self.job_market_agent.invoke_bedrock(prompt)
            insights = self._parse_json_from_response(insights_text)
            return insights
        except Exception as e:
            self.logger.warning(f"Learning extraction failed: {e}")
            return {"note": "Learning extraction failed"}
    
    async def _learn_from_execution(self, response: AgenticResponse):
        """Store learning from execution"""
        learning_entry = {
            'query': response.user_query,
            'agents_used': response.tools_selected,
            'insights': response.learning_insights,
            'timestamp': response.timestamp
        }
        
        self.learning_history.append(learning_entry)
        
        # Keep only recent history
        if len(self.learning_history) > 20:
            self.learning_history = self.learning_history[-20:]
        
        self.logger.info("Learned from execution")
    
    def _parse_execution_plan(self, text: str) -> Dict:
        """Parse execution plan from Bedrock response"""
        try:
            # Extract JSON from text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"Failed to parse execution plan: {e}")
        
        # Fallback
        return {
            "agents_to_use": list(self.agent_registry.keys()),
            "execution_order": list(self.agent_registry.keys()),
            "dependencies": {},
            "expected_outputs": {}
        }
    
    def _parse_json_from_response(self, text: str) -> Dict:
        """Parse JSON from Bedrock response"""
        try:
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return {"raw": text}


# Main execution for testing
async def main():
    """Test the agentic system"""
    system = AgenticCareerGuidanceSystem()
    
    # Test query
    query = "I am a Business Analytics Graduate student at UTD. I want to become a Data Scientist. What courses should I take?"
    
    response = await system.process_query(
        query,
        major="business analytics",
        student_type="graduate"
    )
    
    print("=" * 60)
    print("AGENTIC RESPONSE")
    print("=" * 60)
    print(f"\nQuery: {response.user_query}")
    print(f"\nAgents Used: {response.tools_selected}")
    print(f"\nPlan: {json.dumps(response.plan, indent=2)}")
    print(f"\nUnified Response:\n{response.unified_response}")
    print(f"\nLearning Insights: {json.dumps(response.learning_insights, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())

