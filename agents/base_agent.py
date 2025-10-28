"""
Base Agent class for AWS Course Recommendation AI System
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError
import json

try:
    from .bedrock_agent_core import invoke_agent_core, is_agent_core_available
except ImportError:
    from bedrock_agent_core import invoke_agent_core, is_agent_core_available


class BaseAgent(ABC):
    """
    Abstract base class for all career guidance agents.
    Provides shared functionality for logging, AWS Bedrock integration, and common methods.
    """
    
    def __init__(self, agent_name: str = None):
        """
        Initialize the base agent with logging and AWS Bedrock client.
        
        Args:
            agent_name: Name of the agent for logging purposes
        """
        self.agent_name = agent_name or self.__class__.__name__
        self.logger = logging.getLogger(self.agent_name)
        
        # Configure logging
        self._setup_logging()
        
        # Initialize AWS Bedrock client
        self.bedrock_client = self._initialize_bedrock_client()
        
        # Agent configuration
        self.config = self._load_config()
        
        # Agent Core configuration
        self.use_agent_core = os.getenv('USE_BEDROCK_AGENT_CORE', 'false').lower() == 'true'
        self.agent_core_available = is_agent_core_available()
    
    def _setup_logging(self):
        """Setup logging configuration for the agent."""
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=f'%(asctime)s - {self.agent_name} - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(f'logs/{self.agent_name.lower()}.log')
            ]
        )
    
    def _initialize_bedrock_client(self):
        """Initialize AWS Bedrock client with proper configuration."""
        try:
            region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            return boto3.client(
                'bedrock-runtime',
                region_name=region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize Bedrock client: {e}")
            return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load agent-specific configuration."""
        return {
            'model_id': os.getenv('BEDROCK_MODEL_ID', 'amazon.titan-text-express-v1'),
            'max_tokens': 4000,
            'temperature': 0.7
        }
    
    @abstractmethod
    async def fetch_data(self) -> Any:
        """
        Fetch data from external sources.
        This method should be implemented by each agent to fetch relevant data.
        
        Returns:
            Raw data from external sources
        """
        pass
    
    @abstractmethod
    def process_data(self, data: Any) -> Any:
        """
        Process and transform the fetched data.
        This method should be implemented by each agent to process their specific data.
        
        Args:
            data: Raw data from fetch_data()
            
        Returns:
            Processed data ready for response generation
        """
        pass
    
    @abstractmethod
    async def respond(self, processed_data: Any, user_query: str = None) -> str:
        """
        Generate a response based on processed data.
        This method should be implemented by each agent to generate responses.
        
        Args:
            processed_data: Processed data from process_data()
            user_query: Optional user query for context
            
        Returns:
            Generated response string
        """
        pass
    
    async def invoke_bedrock(self, prompt: str, context: str = None, use_agent_core: bool = None) -> str:
        """
        Invoke AWS Bedrock to generate a response.
        Supports both direct Bedrock runtime and Bedrock Agent Core.
        
        Args:
            prompt: The prompt to send to Bedrock
            context: Optional context to include in the prompt
            use_agent_core: Override agent core usage (optional)
            
        Returns:
            Generated response from Bedrock
        """
        # Determine whether to use Agent Core
        should_use_agent_core = use_agent_core if use_agent_core is not None else self.use_agent_core
        
        # Use Agent Core if configured and available
        if should_use_agent_core and self.agent_core_available:
            return await self._invoke_agent_core(prompt, context)
        
        # Fallback to direct Bedrock runtime
        return await self._invoke_bedrock_runtime(prompt, context)
    
    async def _invoke_agent_core(self, prompt: str, context: str = None) -> str:
        """
        Invoke Bedrock Agent Core
        
        Args:
            prompt: The prompt to send to Agent Core
            context: Optional context to include in the prompt
            
        Returns:
            Generated response from Agent Core
        """
        try:
            # Prepare the full prompt with context
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            self.logger.info(f"Invoking Bedrock Agent Core: {prompt[:100]}...")
            
            # Invoke Agent Core
            response = await invoke_agent_core(
                input_text=full_prompt,
                session_id=f"{self.agent_name}_{hash(prompt) % 10000}",
                enable_trace=False
            )
            
            if response['status'] == 'success':
                self.logger.info("Agent Core invocation successful")
                return response['output_text']
            else:
                self.logger.error(f"Agent Core invocation failed: {response.get('error_code', 'Unknown error')}")
                return f"Error: Agent Core failed - {response['output_text']}"
                
        except Exception as e:
            self.logger.error(f"Agent Core invocation error: {e}")
            return f"Error: Agent Core invocation failed - {str(e)}"
    
    async def _invoke_bedrock_runtime(self, prompt: str, context: str = None) -> str:
        """
        Invoke AWS Bedrock runtime directly
        
        Args:
            prompt: The prompt to send to Bedrock
            context: Optional context to include in the prompt
            
        Returns:
            Generated response from Bedrock runtime
        """
        if not self.bedrock_client:
            self.logger.error("Bedrock client not initialized")
            return "Error: Bedrock client not available"
        
        try:
            # Prepare the full prompt with context
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Check if using Amazon Titan or Anthropic Claude
            model_id = self.config['model_id']
            
            if 'amazon.titan' in model_id:
                # Amazon Titan format
                response = self.bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "inputText": full_prompt,
                        "textGenerationConfig": {
                            "maxTokenCount": self.config['max_tokens'],
                            "temperature": self.config['temperature'],
                            "topP": 0.9
                        }
                    }),
                    contentType="application/json"
                )
                response_body = json.loads(response['body'].read())
                return response_body.get('results', [{}])[0].get('outputText', 'No response generated')
                
            elif 'anthropic.claude' in model_id:
                # Anthropic Claude format
                response = self.bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "prompt": full_prompt,
                        "max_tokens_to_sample": self.config['max_tokens'],
                        "temperature": self.config['temperature']
                    }),
                    contentType="application/json"
                )
                response_body = json.loads(response['body'].read())
                return response_body.get('completion', 'No response generated')
            else:
                # Default to Titan format
                response = self.bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps({
                        "inputText": full_prompt,
                        "textGenerationConfig": {
                            "maxTokenCount": self.config['max_tokens'],
                            "temperature": self.config['temperature'],
                            "topP": 0.9
                        }
                    }),
                    contentType="application/json"
                )
                response_body = json.loads(response['body'].read())
                return response_body.get('results', [{}])[0].get('outputText', 'No response generated')
            
        except ClientError as e:
            self.logger.error(f"Bedrock invocation failed: {e}")
            return f"Error: Failed to generate response - {str(e)}"
        except Exception as e:
            self.logger.error(f"Unexpected error during Bedrock invocation: {e}")
            return f"Error: Unexpected error - {str(e)}"
    
    def save_data(self, data: Any, filename: str) -> bool:
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            filename: Filename to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs('data', exist_ok=True)
            filepath = f"data/{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save data to {filename}: {e}")
            return False
    
    def load_data(self, filename: str) -> Optional[Any]:
        """
        Load data from a JSON file.
        
        Args:
            filename: Filename to load from
            
        Returns:
            Loaded data or None if failed
        """
        try:
            filepath = f"data/{filename}"
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Data loaded from {filepath}")
            return data
        except FileNotFoundError:
            self.logger.warning(f"File {filename} not found")
            return None
        except Exception as e:
            self.logger.error(f"Failed to load data from {filename}: {e}")
            return None
    
    async def run(self, user_query: str = None) -> str:
        """
        Run the complete agent workflow.
        
        Args:
            user_query: Optional user query for context
            
        Returns:
            Final response from the agent
        """
        try:
            self.logger.info(f"Starting {self.agent_name} workflow")
            
            # Fetch data
            raw_data = await self.fetch_data()
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
