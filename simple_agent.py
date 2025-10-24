import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """Simple Lambda function for hackathon demo"""
    
    query = event.get('query', '')
    session_id = event.get('sessionId', '')
    
    # Mock response for hackathon demo
    response = {
        'statusCode': 200,
        'body': {
            'agent': 'SimpleAgent',
            'query': query,
            'result': {
                'analysis': f'Autonomous analysis of: {query}',
                'insights': 'This demonstrates agentic AI capabilities for the hackathon',
                'timestamp': datetime.now().isoformat()
            },
            'sessionId': session_id
        }
    }
    
    return response
