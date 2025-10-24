#!/usr/bin/env python3
"""
Deploy Lambda functions for UTD Career Guidance AI System
"""

import boto3
import json
import zipfile
import os
from typing import Dict, Any

class LambdaDeployer:
    """Deploy Lambda functions for hackathon"""
    
    def __init__(self, region='us-east-1'):
        self.region = region
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.role_arn = f"arn:aws:iam::{self._get_account_id()}:role/LambdaExecutionRole"
        
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']
    
    def create_deployment_package(self, agent_name: str) -> str:
        """Create deployment package for Lambda function"""
        zip_path = f"{agent_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            # Add the agent Python file
            agent_file = f"lambda_functions/{agent_name}.py"
            if os.path.exists(agent_file):
                zip_file.write(agent_file, f"{agent_name}.py")
            else:
                print(f"⚠️ {agent_file} not found")
                return None
        
        return zip_path
    
    def deploy_agent(self, agent_name: str) -> Dict[str, Any]:
        """Deploy a single agent Lambda function"""
        print(f"🚀 Deploying {agent_name}...")
        
        # Create deployment package
        zip_path = self.create_deployment_package(agent_name)
        if not zip_path:
            return {'error': f'Could not create package for {agent_name}'}
        
        try:
            # Read the zip file
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            
            # Create Lambda function
            response = self.lambda_client.create_function(
                FunctionName=f"utd-career-guidance-{agent_name}",
                Runtime='python3.9',
                Role=self.role_arn,
                Handler=f"{agent_name}.lambda_handler",
                Code={'ZipFile': zip_content},
                Timeout=300,
                MemorySize=512,
                Environment={
                    'Variables': {
                        'BEDROCK_MODEL_ID': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
                        'REGION': self.region
                    }
                },
                Description=f"UTD Career Guidance {agent_name} for hackathon"
            )
            
            print(f"✅ {agent_name} deployed: {response['FunctionArn']}")
            
            # Cleanup
            os.remove(zip_path)
            
            return {
                'function_name': response['FunctionName'],
                'function_arn': response['FunctionArn'],
                'status': 'success'
            }
            
        except Exception as e:
            print(f"❌ {agent_name} deployment failed: {e}")
            if os.path.exists(zip_path):
                os.remove(zip_path)
            return {'error': str(e)}
    
    def deploy_all_agents(self) -> Dict[str, Any]:
        """Deploy all agent Lambda functions"""
        print("🚀 Deploying UTD Career Guidance AI System to AWS Lambda")
        print("=" * 60)
        
        agents = [
            'job_market_agent',
            'course_catalog_agent', 
            'career_matching_agent',
            'project_advisor_agent'
        ]
        
        results = {}
        success_count = 0
        
        for agent in agents:
            result = self.deploy_agent(agent)
            results[agent] = result
            
            if 'error' not in result:
                success_count += 1
        
        print(f"\n📊 Deployment Summary:")
        print(f"✅ Successful: {success_count}/{len(agents)}")
        print(f"❌ Failed: {len(agents) - success_count}/{len(agents)}")
        
        return {
            'total_agents': len(agents),
            'successful': success_count,
            'failed': len(agents) - success_count,
            'results': results
        }
    
    def test_agents(self, results: Dict[str, Any]) -> None:
        """Test the deployed agents"""
        print("\n🧪 Testing deployed agents...")
        
        test_payload = {
            'query': 'I want to become a data scientist',
            'sessionId': 'hackathon-test'
        }
        
        for agent_name, result in results['results'].items():
            if 'error' not in result:
                try:
                    print(f"Testing {agent_name}...")
                    
                    response = self.lambda_client.invoke(
                        FunctionName=result['function_name'],
                        InvocationType='RequestResponse',
                        Payload=json.dumps(test_payload)
                    )
                    
                    response_payload = json.loads(response['Payload'].read())
                    
                    if response_payload.get('statusCode') == 200:
                        print(f"✅ {agent_name} test passed")
                    else:
                        print(f"❌ {agent_name} test failed: {response_payload}")
                        
                except Exception as e:
                    print(f"❌ {agent_name} test error: {e}")
            else:
                print(f"⏭️ Skipping {agent_name} (deployment failed)")

def main():
    """Main deployment function"""
    deployer = LambdaDeployer()
    
    # Deploy all agents
    results = deployer.deploy_all_agents()
    
    # Test agents
    deployer.test_agents(results)
    
    # Save results
    with open('lambda-deployment-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Deployment results saved to lambda-deployment-results.json")
    
    if results['successful'] > 0:
        print("\n🎉 AWS Lambda deployment successful!")
        print("Your hackathon agents are now running on AWS!")
    else:
        print("\n❌ No agents deployed successfully")
        print("Check the error messages above for details")

if __name__ == "__main__":
    main()
