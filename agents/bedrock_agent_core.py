"""
Bedrock Agent Core Integration
Provides wrapper for AWS Bedrock Agent Core functionality
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
import boto3
from botocore.exceptions import ClientError


class BedrockAgentCore:
    """
    Wrapper for AWS Bedrock Agent Core functionality
    Handles agent invocation, tool orchestration, and response processing
    """
    
    def __init__(self, agent_id: str = None, agent_alias_id: str = None, region: str = None):
        """
        Initialize Bedrock Agent Core client
        
        Args:
            agent_id: Bedrock Agent ID (e.g., 'ag-xxxxxxxx')
            agent_alias_id: Bedrock Agent Alias ID (e.g., 'ag-alias-xxxxxxxx')
            region: AWS region (default: us-east-1)
        """
        self.logger = logging.getLogger("BedrockAgentCore")
        
        # Configuration
        self.agent_id = agent_id or os.getenv('BEDROCK_AGENT_ID')
        self.agent_alias_id = agent_alias_id or os.getenv('BEDROCK_AGENT_ALIAS_ID')
        self.region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        
        # Validate required parameters
        if not self.agent_id:
            raise ValueError("BEDROCK_AGENT_ID is required")
        if not self.agent_alias_id:
            raise ValueError("BEDROCK_AGENT_ALIAS_ID is required")
        
        # Initialize client
        self.client = self._initialize_client()
        
        self.logger.info(f"BedrockAgentCore initialized for agent {self.agent_id} in {self.region}")
    
    def _initialize_client(self):
        """Initialize Bedrock Agent Runtime client"""
        try:
            return boto3.client(
                'bedrock-agent-runtime',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Bedrock Agent client: {e}")
            raise
    
    async def invoke_agent(self, 
                          input_text: str,
                          session_id: str = None,
                          enable_trace: bool = False,
                          end_session: bool = False) -> Dict[str, Any]:
        """
        Invoke Bedrock Agent with input text
        
        Args:
            input_text: User input text
            session_id: Session identifier for conversation continuity
            enable_trace: Enable tracing for debugging
            end_session: Whether to end the session after this invocation
            
        Returns:
            Agent response with output text and metadata
        """
        try:
            # Prepare invocation parameters
            params = {
                'agentId': self.agent_id,
                'agentAliasId': self.agent_alias_id,
                'inputText': input_text,
                'enableTrace': enable_trace,
                'endSession': end_session
            }
            
            # Add session ID if provided
            if session_id:
                params['sessionId'] = session_id
            
            self.logger.info(f"Invoking Bedrock Agent with input: {input_text[:100]}...")
            
            # Invoke agent
            response = self.client.invoke_agent(**params)
            
            # Process streaming response
            output_text = ""
            trace_data = []
            
            for event in response['completion']:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        output_text += chunk['bytes'].decode('utf-8')
                
                if 'trace' in event and enable_trace:
                    trace_data.append(event['trace'])
            
            result = {
                'output_text': output_text.strip(),
                'session_id': response.get('sessionId'),
                'trace_data': trace_data if enable_trace else [],
                'status': 'success'
            }
            
            self.logger.info(f"Agent response received: {len(output_text)} characters")
            return result
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            self.logger.error(f"Bedrock Agent invocation failed: {error_code} - {error_msg}")
            
            return {
                'output_text': f"Error: {error_msg}",
                'session_id': session_id,
                'trace_data': [],
                'status': 'error',
                'error_code': error_code
            }
            
        except Exception as e:
            self.logger.error(f"Unexpected error during agent invocation: {e}")
            return {
                'output_text': f"Error: {str(e)}",
                'session_id': session_id,
                'trace_data': [],
                'status': 'error'
            }
    
    async def invoke_agent_with_tools(self,
                                    input_text: str,
                                    tools: List[Dict[str, Any]] = None,
                                    session_id: str = None) -> Dict[str, Any]:
        """
        Invoke agent with specific tools
        
        Args:
            input_text: User input text
            tools: List of tool definitions
            session_id: Session identifier
            
        Returns:
            Agent response with tool usage information
        """
        # For now, use standard invoke_agent
        # Tool orchestration is handled by the agent configuration
        return await self.invoke_agent(input_text, session_id, enable_trace=True)
    
    def get_agent_info(self) -> Dict[str, str]:
        """Get agent configuration information"""
        return {
            'agent_id': self.agent_id,
            'agent_alias_id': self.agent_alias_id,
            'region': self.region
        }
    
    def is_available(self) -> bool:
        """Check if agent is available and configured"""
        return bool(self.agent_id and self.agent_alias_id and self.client)


class BedrockAgentCoreManager:
    """
    Manager for multiple Bedrock Agent Core instances
    Provides centralized configuration and routing
    """
    
    def __init__(self):
        self.logger = logging.getLogger("BedrockAgentCoreManager")
        self.agents = {}
        self.default_agent = None
        
        # Initialize default agent if configured
        self._initialize_default_agent()
    
    def _initialize_default_agent(self):
        """Initialize default agent from environment variables"""
        try:
            agent_id = os.getenv('BEDROCK_AGENT_ID')
            agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID')
            
            if agent_id and agent_alias_id:
                self.default_agent = BedrockAgentCore(agent_id, agent_alias_id)
                self.logger.info("Default Bedrock Agent Core initialized")
            else:
                self.logger.warning("Bedrock Agent Core not configured - missing BEDROCK_AGENT_ID or BEDROCK_AGENT_ALIAS_ID")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize default agent: {e}")
    
    def register_agent(self, name: str, agent_id: str, agent_alias_id: str, region: str = None):
        """Register a new agent"""
        try:
            agent = BedrockAgentCore(agent_id, agent_alias_id, region)
            self.agents[name] = agent
            self.logger.info(f"Registered agent: {name}")
        except Exception as e:
            self.logger.error(f"Failed to register agent {name}: {e}")
    
    def get_agent(self, name: str = None) -> Optional[BedrockAgentCore]:
        """Get agent by name or return default agent"""
        if name and name in self.agents:
            return self.agents[name]
        return self.default_agent
    
    def is_available(self) -> bool:
        """Check if any agent is available"""
        return self.default_agent is not None and self.default_agent.is_available()
    
    def list_agents(self) -> List[str]:
        """List all registered agent names"""
        return list(self.agents.keys())


# Global manager instance
agent_core_manager = BedrockAgentCoreManager()


# Convenience functions
async def invoke_agent_core(input_text: str, 
                           session_id: str = None,
                           agent_name: str = None,
                           enable_trace: bool = False) -> Dict[str, Any]:
    """
    Convenience function to invoke Bedrock Agent Core
    
    Args:
        input_text: User input text
        session_id: Session identifier
        agent_name: Specific agent name (optional)
        enable_trace: Enable tracing
        
    Returns:
        Agent response
    """
    agent = agent_core_manager.get_agent(agent_name)
    if not agent:
        return {
            'output_text': 'Error: No Bedrock Agent Core configured',
            'status': 'error'
        }
    
    return await agent.invoke_agent(input_text, session_id, enable_trace)


def is_agent_core_available() -> bool:
    """Check if Bedrock Agent Core is available"""
    return agent_core_manager.is_available()


def get_agent_core_info() -> Dict[str, Any]:
    """Get information about configured agents"""
    info = {
        'available': agent_core_manager.is_available(),
        'agents': {}
    }
    
    if agent_core_manager.default_agent:
        info['default_agent'] = agent_core_manager.default_agent.get_agent_info()
    
    for name, agent in agent_core_manager.agents.items():
        info['agents'][name] = agent.get_agent_info()
    
    return info


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_agent_core():
        """Test Bedrock Agent Core functionality"""
        if not is_agent_core_available():
            print("❌ Bedrock Agent Core not configured")
            return
        
        print("✅ Bedrock Agent Core available")
        print(f"Agent info: {get_agent_core_info()}")
        
        # Test invocation
        response = await invoke_agent_core(
            "Hello, I'm a Business Analytics graduate student at UTD. What courses should I take to become a data scientist?",
            session_id="test_session_123"
        )
        
        print(f"Response: {response['output_text']}")
        print(f"Status: {response['status']}")
    
    asyncio.run(test_agent_core())
