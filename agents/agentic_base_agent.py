"""
Enhanced Agentic Base Agent with planning, memory, and tool integration
Extends the existing BaseAgent with agentic capabilities
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum

try:
    from .base_agent import BaseAgent
except ImportError:
    from base_agent import BaseAgent


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    NEEDS_REFINEMENT = "needs_refinement"


class AgenticPlan:
    """Represents a decomposed task plan"""
    
    def __init__(self, query: str, steps: List[Dict]):
        self.query = query
        self.steps = steps  # List of {step_name, tools, expected_output, dependencies}
        self.current_step = 0
        self.status = TaskStatus.PENDING
        
    def get_next_step(self):
        """Get the next step to execute"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def mark_step_complete(self, result: Any):
        """Mark current step as complete and store result"""
        if self.current_step < len(self.steps):
            self.steps[self.current_step]['result'] = result
            self.steps[self.current_step]['status'] = 'complete'
            self.current_step += 1
            
            if self.current_step >= len(self.steps):
                self.status = TaskStatus.SUCCESS
            else:
                self.status = TaskStatus.EXECUTING


class AgenticBaseAgent(BaseAgent):
    """
    Enhanced base agent with agentic capabilities:
    - Planning and reasoning
    - Tool selection and integration
    - Memory and context retention
    - Iterative refinement
    """
    
    def __init__(self, agent_name: str = None):
        super().__init__(agent_name)
        
        # Agentic capabilities
        self.memory = {}  # Short-term memory for current session
        self.learning_patterns = {}  # Long-term learning
        self.tool_registry = self._initialize_tools()
        self.execution_history = []
        
    def _initialize_tools(self) -> Dict:
        """Initialize available tools for this agent"""
        return {
            'bedrock_ai': {
                'name': 'Bedrock AI',
                'description': 'AWS Bedrock for AI analysis',
                'execute': self.invoke_bedrock
            },
            'web_scraping': {
                'name': 'Web Scraping',
                'description': 'Fetch data from web',
                'execute': None  # Implemented in subclasses
            },
            'data_processing': {
                'name': 'Data Processing',
                'description': 'Process and transform data',
                'execute': None  # Implemented in subclasses
            }
        }
    
    async def plan_task(self, query: str) -> AgenticPlan:
        """
        Use Bedrock to decompose task into steps
        
        Args:
            query: User query
            
        Returns:
            AgenticPlan with decomposed steps
        """
        self.logger.info(f"Planning task: {query}")
        
        # Retrieve relevant context from memory
        context = await self._retrieve_relevant_context(query)
        
        prompt = f"""
        You are an intelligent agent planner. Decompose this task into actionable steps.
        
        Query: {query}
        Agent Type: {self.agent_name}
        Available Tools: {list(self.tool_registry.keys())}
        Relevant Context: {context}
        
        Create a detailed plan with:
        1. Step-by-step execution plan
        2. Required tools for each step
        3. Expected outputs
        4. Dependencies between steps
        
        Return a JSON structure with steps as an array.
        Each step should have: step_name, description, tools_needed, expected_output
        """
        
        try:
            response = await self.invoke_bedrock(prompt)
            
            # Parse response to extract plan
            steps = self._parse_plan_response(response)
            
            plan = AgenticPlan(query, steps)
            self.logger.info(f"Created plan with {len(steps)} steps")
            
            return plan
            
        except Exception as e:
            self.logger.error(f"Planning failed: {e}")
            # Fallback to simple plan
            return AgenticPlan(query, [
                {
                    'step_name': 'execute',
                    'description': query,
                    'tools_needed': ['bedrock_ai'],
                    'expected_output': 'Response'
                }
            ])
    
    async def _retrieve_relevant_context(self, query: str) -> str:
        """
        Retrieve relevant context from memory using Bedrock
        
        Args:
            query: Current query
            
        Returns:
            Relevant context from past interactions
        """
        if not self.memory:
            return "No previous context available"
        
        prompt = f"""
        Given this query: {query}
        And this memory history: {json.dumps(self.memory, indent=2)}
        
        Retrieve and summarize only the most relevant past interactions.
        Return a concise summary of relevant context.
        """
        
        try:
            context = await self.invoke_bedrock(prompt)
            return context
        except Exception as e:
            self.logger.warning(f"Context retrieval failed: {e}")
            return "No relevant context found"
    
    async def select_tools(self, task_description: str) -> List[str]:
        """
        Use Bedrock to select appropriate tools for a task
        
        Args:
            task_description: Description of the task
            
        Returns:
            List of selected tool names
        """
        prompt = f"""
        Task: {task_description}
        Available Tools: {list(self.tool_registry.keys())}
        
        Select the most appropriate tools for this task.
        Return a JSON array of tool names with brief reasoning.
        """
        
        try:
            response = await self.invoke_bedrock(prompt)
            # Parse tool selection from response
            tools = self._parse_tool_selection(response)
            self.logger.info(f"Selected tools: {tools}")
            return tools
        except Exception as e:
            self.logger.warning(f"Tool selection failed: {e}")
            return ['bedrock_ai']  # Default fallback
    
    async def execute_with_plan(self, plan: AgenticPlan) -> Any:
        """
        Execute a task plan iteratively
        
        Args:
            plan: The agentic plan to execute
            
        Returns:
            Final result after executing all steps
        """
        plan.status = TaskStatus.EXECUTING
        results = []
        
        while plan.current_step < len(plan.steps):
            step = plan.get_next_step()
            if not step:
                break
            
            self.logger.info(f"Executing step {plan.current_step + 1}/{len(plan.steps)}: {step.get('step_name', 'unknown')}")
            
            try:
                # Execute the step
                result = await self._execute_step(step, plan)
                
                # Validate result
                if await self._validate_result(result, step):
                    plan.mark_step_complete(result)
                    results.append(result)
                else:
                    # Iterative refinement
                    self.logger.info("Result needs refinement")
                    refined_result = await self._refine_result(result, step)
                    plan.mark_step_complete(refined_result)
                    results.append(refined_result)
                    
            except Exception as e:
                self.logger.error(f"Step execution failed: {e}")
                plan.status = TaskStatus.FAILED
                break
        
        # Combine results
        final_result = await self._combine_results(results, plan.query)
        
        # Learn from this execution
        await self._learn_from_execution(plan, final_result)
        
        return final_result
    
    async def _execute_step(self, step: Dict, plan: AgenticPlan) -> Any:
        """
        Execute a single step of the plan
        
        Args:
            step: Step to execute
            plan: Overall plan for context
            
        Returns:
            Step execution result
        """
        # Get tools needed for this step
        tools_needed = step.get('tools_needed', ['bedrock_ai'])
        
        # Execute with tools
        result = {}
        for tool_name in tools_needed:
            if tool_name in self.tool_registry:
                tool = self.tool_registry[tool_name]
                if hasattr(tool, 'execute') and tool['execute']:
                    # Execute tool
                    tool_result = await tool['execute'](
                        f"{step.get('description', '')}\n\nContext: {plan.query}"
                    )
                    result[tool_name] = tool_result
        
        return result
    
    async def _validate_result(self, result: Any, step: Dict) -> bool:
        """
        Validate if result meets the expected output
        
        Args:
            result: Execution result
            step: Step definition
            
        Returns:
            True if valid, False otherwise
        """
        expected_output = step.get('expected_output', '')
        
        # Use Bedrock to validate
        prompt = f"""
        Validate if this result meets the expected criteria.
        
        Expected: {expected_output}
        Actual Result: {json.dumps(result, indent=2)}
        
        Is the result satisfactory? Return only 'yes' or 'no' with brief reason.
        """
        
        try:
            validation = await self.invoke_bedrock(prompt)
            is_valid = 'yes' in validation.lower()
            self.logger.info(f"Validation result: {is_valid}")
            return is_valid
        except Exception as e:
            self.logger.warning(f"Validation failed: {e}")
            return True  # Default to valid if validation fails
    
    async def _refine_result(self, result: Any, step: Dict) -> Any:
        """
        Refine a result that didn't meet validation
        
        Args:
            result: Previous result
            step: Step definition
            
        Returns:
            Refined result
        """
        self.logger.info(f"Refining result for step: {step.get('step_name')}")
        
        prompt = f"""
        The previous attempt didn't meet the expected criteria.
        
        Step: {step.get('description')}
        Expected: {step.get('expected_output')}
        Previous Result: {json.dumps(result, indent=2)}
        
        Provide an improved result that better meets the criteria.
        """
        
        try:
            refined = await self.invoke_bedrock(prompt)
            return refined
        except Exception as e:
            self.logger.error(f"Refinement failed: {e}")
            return result  # Return original if refinement fails
    
    async def _combine_results(self, results: List[Any], query: str) -> Any:
        """
        Combine results from all steps into final output
        
        Args:
            results: All step results
            query: Original query
            
        Returns:
            Combined final result
        """
        prompt = f"""
        Combine these step results into a coherent final answer.
        
        Original Query: {query}
        
        Step Results:
        {json.dumps(results, indent=2)}
        
        Provide a unified, comprehensive response.
        """
        
        try:
            combined = await self.invoke_bedrock(prompt)
            return combined
        except Exception as e:
            self.logger.error(f"Result combination failed: {e}")
            return json.dumps(results, indent=2)
    
    async def _learn_from_execution(self, plan: AgenticPlan, result: Any):
        """
        Learn from execution for future improvements
        
        Args:
            plan: The executed plan
            result: Final result
        """
        pattern = {
            'query': plan.query,
            'steps': plan.steps,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in learning patterns
        if 'patterns' not in self.learning_patterns:
            self.learning_patterns['patterns'] = []
        
        self.learning_patterns['patterns'].append(pattern)
        
        # Keep only recent patterns (last 10)
        if len(self.learning_patterns['patterns']) > 10:
            self.learning_patterns['patterns'] = self.learning_patterns['patterns'][-10:]
        
        self.logger.info("Learned from execution")
    
    def _parse_plan_response(self, response: str) -> List[Dict]:
        """Parse plan from Bedrock response"""
        try:
            # Try to extract JSON from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"Failed to parse JSON: {e}")
        
        # Fallback: create simple plan
        return [
            {
                'step_name': 'execute',
                'description': response,
                'tools_needed': ['bedrock_ai'],
                'expected_output': 'Response'
            }
        ]
    
    def _parse_tool_selection(self, response: str) -> List[str]:
        """Parse tool selection from Bedrock response"""
        try:
            # Extract JSON array from response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except Exception as e:
            self.logger.warning(f"Failed to parse tool selection: {e}")
        
        return ['bedrock_ai']


# Example usage
async def example_usage():
    """Example of using the agentic agent"""
    
    class ExampleAgenticAgent(AgenticBaseAgent):
        async def fetch_data(self):
            return {"test": "data"}
        
        def process_data(self, data):
            return data
        
        async def respond(self, processed_data, user_query=None):
            return "Response"
    
    agent = ExampleAgenticAgent("ExampleAgent")
    
    # Plan the task
    plan = await agent.plan_task("Analyze job market trends")
    
    # Execute with plan
    result = await agent.execute_with_plan(plan)
    
    print(result)


if __name__ == "__main__":
    asyncio.run(example_usage())

