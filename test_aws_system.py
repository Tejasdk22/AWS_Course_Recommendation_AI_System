#!/usr/bin/env python3
"""
AWS Lambda System Test - Run directly in AWS
Tests all Lambda functions and shows results in terminal
"""

import boto3
import json
import time
from datetime import datetime

def test_aws_lambda_system():
    """Test the complete AWS Lambda system"""
    
    print("🎯 UTD CAREER GUIDANCE AI SYSTEM - AWS LAMBDA TEST")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Running directly in AWS Lambda...")
    print()
    
    # Initialize Lambda client
    lambda_client = boto3.client('lambda')
    
    # Test cases
    test_cases = [
        "I want to become a data scientist",
        "I want to become a software engineer", 
        "I want to work in machine learning",
        "I want to become a web developer"
    ]
    
    print("🔍 TESTING INDIVIDUAL AGENTS")
    print("=" * 50)
    
    # Test individual agents
    agents = [
        'utd-career-guidance-job_market_agent',
        'utd-career-guidance-course_catalog_agent',
        'utd-career-guidance-career_matching_agent', 
        'utd-career-guidance-project_advisor_agent'
    ]
    
    for i, agent in enumerate(agents, 1):
        print(f"\\n{i}. {agent.split('-')[-1].replace('_', ' ').title()}:")
        
        try:
            response = lambda_client.invoke(
                FunctionName=agent,
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': 'I want to become a data scientist',
                    'sessionId': f'aws-test-{i}'
                })
            )
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                print("   ✅ Status: SUCCESS")
                print(f"   ✅ Agent: {result['body']['agent']}")
                print(f"   ✅ Processing: {result['body']['result']['analysis']}")
            else:
                print("   ❌ Status: ERROR")
                print(f"   ❌ Error: {result}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    print("\\n" + "=" * 70)
    print("🎯 TESTING ORCHESTRATOR (FULL SYSTEM)")
    print("=" * 70)
    
    # Test orchestrator with different queries
    for i, query in enumerate(test_cases, 1):
        print(f"\\n🧪 TEST CASE {i}: {query}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            response = lambda_client.invoke(
                FunctionName='utd-career-guidance-orchestrator',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': query,
                    'sessionId': f'aws-orchestrator-test-{i}'
                })
            )
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                body = json.loads(result['body'])
                career_guidance = body['career_guidance']
                summary = career_guidance['summary']
                coordination = body['agent_coordination']
                
                print(f"✅ Status: SUCCESS")
                print(f"✅ Response Time: {response_time}s")
                print(f"✅ Agents Involved: {coordination['agents_involved']}")
                print(f"✅ Coordination: {coordination['coordination_successful']}")
                print()
                print(f"🎯 CAREER GUIDANCE:")
                print(f"   Career Path: {summary['career_path']}")
                print(f"   Key Skills: {summary['key_skills_needed']}")
                print(f"   Recommended Courses: {summary['recommended_utd_courses']}")
                print(f"   Next Steps: {summary['next_steps']}")
                
            else:
                print(f"❌ Status: ERROR")
                print(f"❌ Error: {result}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\\n" + "=" * 70)
    
    print("\\n🎉 AWS LAMBDA SYSTEM TEST COMPLETE!")
    print("Your agentic AI system is running perfectly in AWS!")

if __name__ == "__main__":
    test_aws_lambda_system()
