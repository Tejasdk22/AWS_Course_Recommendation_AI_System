"""
API Gateway Setup Script for Career Guidance System
Creates API Gateway with proper endpoints for the career guidance system
"""

import boto3
import json
import time
from botocore.exceptions import ClientError

def create_api_gateway():
    """Create API Gateway for Career Guidance System"""
    
    # Initialize clients
    apigateway = boto3.client('apigateway', region_name='us-east-1')
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    
    try:
        # Create API Gateway
        print("Creating API Gateway...")
        api_response = apigateway.create_rest_api(
            name='career-guidance-api',
            description='Career Guidance AI System API',
            endpointConfiguration={
                'types': ['REGIONAL']
            }
        )
        
        api_id = api_response['id']
        print(f"API Gateway created with ID: {api_id}")
        
        # Get root resource
        root_resource = apigateway.get_resources(restApiId=api_id)['items'][0]
        root_resource_id = root_resource['id']
        
        # Create /api resource
        api_resource = apigateway.create_resource(
            restApiId=api_id,
            parentId=root_resource_id,
            pathPart='api'
        )
        api_resource_id = api_resource['id']
        
        # Create /career-guidance resource
        career_resource = apigateway.create_resource(
            restApiId=api_id,
            parentId=api_resource_id,
            pathPart='career-guidance'
        )
        career_resource_id = career_resource['id']
        
        # Create /courses resource
        courses_resource = apigateway.create_resource(
            restApiId=api_id,
            parentId=api_resource_id,
            pathPart='courses'
        )
        courses_resource_id = courses_resource['id']
        
        # Create POST method for /api/career-guidance
        print("Creating POST method for career guidance...")
        apigateway.put_method(
            restApiId=api_id,
            resourceId=career_resource_id,
            httpMethod='POST',
            authorizationType='NONE',
            requestParameters={
                'method.request.header.Content-Type': False
            }
        )
        
        # Create GET method for /api/courses
        print("Creating GET method for courses...")
        apigateway.put_method(
            restApiId=api_id,
            resourceId=courses_resource_id,
            httpMethod='GET',
            authorizationType='NONE',
            requestParameters={
                'method.request.querystring.major': False,
                'method.request.querystring.level': False
            }
        )
        
        # Get Lambda function ARNs
        try:
            career_lambda_arn = lambda_client.get_function(FunctionName='career-guidance-orchestrator')['Configuration']['FunctionArn']
            print(f"Found career guidance Lambda: {career_lambda_arn}")
        except ClientError:
            print("Career guidance Lambda not found. Please deploy it first.")
            return None
        
        # Create Lambda integration for career guidance
        print("Creating Lambda integration for career guidance...")
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=career_resource_id,
            httpMethod='POST',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{career_lambda_arn}/invocations'
        )
        
        # Create Lambda integration for courses (using same Lambda for now)
        print("Creating Lambda integration for courses...")
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=courses_resource_id,
            httpMethod='GET',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{career_lambda_arn}/invocations'
        )
        
        # Add Lambda permissions for API Gateway
        print("Adding Lambda permissions...")
        try:
            # Get account ID for proper ARN
            sts_client = boto3.client('sts')
            account_id = sts_client.get_caller_identity()['Account']
            
            lambda_client.add_permission(
                FunctionName='career-guidance-orchestrator',
                StatementId='apigateway-invoke',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f'arn:aws:execute-api:us-east-1:{account_id}:{api_id}/*/*'
            )
        except ClientError as e:
            if 'already exists' in str(e):
                print("Lambda permission already exists")
            else:
                raise
        
        # Deploy API
        print("Deploying API...")
        deployment = apigateway.create_deployment(
            restApiId=api_id,
            stageName='prod',
            description='Production deployment'
        )
        
        # Get API Gateway URL
        api_url = f"https://{api_id}.execute-api.us-east-1.amazonaws.com/prod"
        print(f"API Gateway URL: {api_url}")
        
        return {
            'api_id': api_id,
            'api_url': api_url,
            'career_endpoint': f"{api_url}/api/career-guidance",
            'courses_endpoint': f"{api_url}/api/courses"
        }
        
    except ClientError as e:
        print(f"Error creating API Gateway: {e}")
        return None

def test_api_gateway(api_url):
    """Test the API Gateway endpoints"""
    import requests
    
    print(f"\nTesting API Gateway at: {api_url}")
    
    # Test courses endpoint
    try:
        print("Testing courses endpoint...")
        response = requests.get(f"{api_url}/api/courses?major=CS&level=graduate", timeout=30)
        print(f"Courses endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data.get('total_count', 0)} courses")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Courses endpoint error: {e}")
    
    # Test career guidance endpoint
    try:
        print("Testing career guidance endpoint...")
        response = requests.post(
            f"{api_url}/api/career-guidance",
            json={
                "query": "I want to become a Data Engineer. What courses should I take?",
                "major": "CS",
                "studentType": "graduate",
                "careerGoal": "Data Engineer"
            },
            timeout=60
        )
        print(f"Career guidance endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response received: {len(data.get('unified_response', ''))} characters")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Career guidance endpoint error: {e}")

if __name__ == "__main__":
    print("Setting up API Gateway for Career Guidance System...")
    
    result = create_api_gateway()
    if result:
        print(f"\n✅ API Gateway setup complete!")
        print(f"API ID: {result['api_id']}")
        print(f"API URL: {result['api_url']}")
        print(f"Career Guidance Endpoint: {result['career_endpoint']}")
        print(f"Courses Endpoint: {result['courses_endpoint']}")
        
        # Test the endpoints
        test_api_gateway(result['api_url'])
        
        # Save configuration
        with open('api_gateway_config.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nConfiguration saved to api_gateway_config.json")
    else:
        print("❌ API Gateway setup failed")
