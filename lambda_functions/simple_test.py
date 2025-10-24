"""
Simple Test Lambda Function
Returns a basic response to test connectivity
"""

import json

def handler(event, context):
    """Simple test handler"""
    try:
        # Parse input
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
            query = body.get('query', '')
        else:
            query = event.get('query', '')
        
        # Return a simple response
        response = {
            'status': 'success',
            'message': 'Lambda function is working!',
            'query': query,
            'timestamp': '2025-10-24T03:20:00Z',
            'test_data': {
                'major': 'Business Analytics',
                'student_type': 'Graduate',
                'career_goal': 'Data Engineer',
                'courses': [
                    {
                        'code': 'BUAN 6341',
                        'name': 'Advanced Business Analytics',
                        'credits': 3
                    },
                    {
                        'code': 'BUAN 6343',
                        'name': 'Big Data Analytics',
                        'credits': 3
                    }
                ]
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Error in test function'
            })
        }
