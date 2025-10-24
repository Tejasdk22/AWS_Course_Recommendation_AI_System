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
    
    async def invoke_bedrock(self, prompt: str, context: str = None) -> str:
        """
        Invoke AWS Bedrock to generate a response.
        
        Args:
            prompt: The prompt to send to Bedrock
            context: Optional context to include in the prompt
            
        Returns:
            Generated response from Bedrock
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
