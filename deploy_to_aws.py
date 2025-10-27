#!/usr/bin/env python3
"""
AWS Deployment Script for Career Guidance AI System
Deploys the complete system to AWS with all necessary resources
"""

import boto3
import json
import zipfile
import os
import time
from datetime import datetime
from pathlib import Path

class AWSDeployer:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.session = boto3.Session()
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.apigateway_client = boto3.client('apigateway', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.bedrock_client = boto3.client('bedrock', region_name=region)
        
        # Get account ID
        sts = boto3.client('sts')
        self.account_id = sts.get_caller_identity()['Account']
        
        print(f"🚀 AWS Career Guidance AI System Deployment")
        print(f"Region: {region}")
        print(f"Account: {self.account_id}")
        print("=" * 60)
    
    def create_iam_role(self):
        """Create IAM role for Lambda functions"""
        print("🔐 Creating IAM role for Lambda functions...")
        
        role_name = "CareerGuidanceLambdaRole"
        
        # Trust policy for Lambda
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        # Permissions policy
        permissions_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "arn:aws:logs:*:*:*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject"
                    ],
                    "Resource": f"arn:aws:s3:::career-guidance-*/*"
                }
            ]
        }
        
        try:
            # Create role
            role_response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Role for Career Guidance AI Lambda functions"
            )
            
            # Attach policies
            self.iam_client.put_role_policy(
                RoleName=role_name,
                PolicyName="CareerGuidancePolicy",
                PolicyDocument=json.dumps(permissions_policy)
            )
            
            # Attach AWS managed policy
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            )
            
            role_arn = f"arn:aws:iam::{self.account_id}:role/{role_name}"
            print(f"✅ IAM role created: {role_arn}")
            return role_arn
            
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print(f"✅ IAM role already exists: {role_name}")
            return f"arn:aws:iam::{self.account_id}:role/{role_name}"
        except Exception as e:
            print(f"❌ Error creating IAM role: {e}")
            return None
    
    def create_deployment_package(self, source_dir, output_file):
        """Create deployment package for Lambda"""
        print(f"📦 Creating deployment package: {output_file}")
        
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file.endswith('.py') or file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
        
        print(f"✅ Deployment package created: {output_file}")
        return output_file
    
    def deploy_lambda_function(self, function_name, handler, role_arn, zip_file):
        """Deploy Lambda function"""
        print(f"🚀 Deploying Lambda function: {function_name}")
        
        try:
            with open(zip_file, 'rb') as f:
                zip_content = f.read()
            
            # Create or update function
            try:
                response = self.lambda_client.create_function(
                    FunctionName=function_name,
                    Runtime='python3.9',
                    Role=role_arn,
                    Handler=handler,
                    Code={'ZipFile': zip_content},
                    Description=f'Career Guidance AI - {function_name}',
                    Timeout=300,
                    MemorySize=512,
                    Environment={
                        'Variables': {
                            'AWS_DEFAULT_REGION': self.region,
                            'BEDROCK_MODEL_ID': 'amazon.titan-text-express-v1'
                        }
                    }
                )
                print(f"✅ Lambda function created: {function_name}")
                
            except self.lambda_client.exceptions.ResourceConflictException:
                # Update existing function
                self.lambda_client.update_function_code(
                    FunctionName=function_name,
                    ZipFile=zip_content
                )
                print(f"✅ Lambda function updated: {function_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error deploying {function_name}: {e}")
            return False
    
    def create_api_gateway(self):
        """Create API Gateway for the system"""
        print("🌐 Creating API Gateway...")
        
        try:
            # Create REST API
            api_response = self.apigateway_client.create_rest_api(
                name='CareerGuidanceAPI',
                description='API for Career Guidance AI System',
                endpointConfiguration={'types': ['REGIONAL']}
            )
            api_id = api_response['id']
            
            # Get root resource
            resources = self.apigateway_client.get_resources(restApiId=api_id)
            root_id = next(item['id'] for item in resources['items'] if item['path'] == '/')
            
            # Create /career-guidance resource
            resource_response = self.apigateway_client.create_resource(
                restApiId=api_id,
                parentId=root_id,
                pathPart='career-guidance'
            )
            resource_id = resource_response['id']
            
            # Create POST method
            self.apigateway_client.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                authorizationType='NONE'
            )
            
            # Create integration with Lambda
            lambda_arn = f"arn:aws:lambda:{self.region}:{self.account_id}:function:career-guidance-orchestrator"
            self.apigateway_client.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
            )
            
            # Deploy API
            deployment_response = self.apigateway_client.create_deployment(
                restApiId=api_id,
                stageName='prod'
            )
            
            api_url = f"https://{api_id}.execute-api.{self.region}.amazonaws.com/prod"
            print(f"✅ API Gateway created: {api_url}")
            return api_url
            
        except Exception as e:
            print(f"❌ Error creating API Gateway: {e}")
            return None
    
    def test_deployment(self, api_url):
        """Test the deployed system"""
        print("🧪 Testing deployment...")
        
        import requests
        
        test_payload = {
            "query": "I want to become a data scientist. What should I learn?",
            "sessionId": "test-session"
        }
        
        try:
            response = requests.post(
                f"{api_url}/career-guidance",
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Deployment test successful!")
                return True
            else:
                print(f"❌ Test failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
    
    def deploy_system(self):
        """Deploy the complete system"""
        print("🚀 Starting AWS Career Guidance AI System Deployment")
        print("=" * 60)
        
        # Step 1: Create IAM role
        role_arn = self.create_iam_role()
        if not role_arn:
            print("❌ Failed to create IAM role. Exiting.")
            return False
        
        # Step 2: Create deployment packages
        print("\n📦 Creating deployment packages...")
        
        # Main orchestrator package
        orchestrator_zip = "career_guidance_orchestrator.zip"
        self.create_deployment_package(".", orchestrator_zip)
        
        # Step 3: Deploy Lambda functions
        print("\n🚀 Deploying Lambda functions...")
        
        # Deploy main orchestrator
        success = self.deploy_lambda_function(
            "career-guidance-orchestrator",
            "career_guidance_system.lambda_handler",
            role_arn,
            orchestrator_zip
        )
        
        if not success:
            print("❌ Failed to deploy orchestrator. Exiting.")
            return False
        
        # Step 4: Create API Gateway
        print("\n🌐 Creating API Gateway...")
        api_url = self.create_api_gateway()
        
        if not api_url:
            print("❌ Failed to create API Gateway. Exiting.")
            return False
        
        # Step 5: Test deployment
        print("\n🧪 Testing deployment...")
        test_success = self.test_deployment(api_url)
        
        # Step 6: Create deployment summary
        summary = {
            "deployment_status": "success" if test_success else "partial",
            "api_url": api_url,
            "region": self.region,
            "account_id": self.account_id,
            "lambda_functions": ["career-guidance-orchestrator"],
            "test_success": test_success,
            "deployment_time": datetime.now().isoformat()
        }
        
        with open("aws_deployment_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print("\n🎉 Deployment Summary")
        print("=" * 40)
        print(f"✅ API URL: {api_url}")
        print(f"✅ Region: {self.region}")
        print(f"✅ Test Status: {'PASSED' if test_success else 'FAILED'}")
        print(f"✅ Summary: aws_deployment_summary.json")
        
        if test_success:
            print("\n🏆 Your Career Guidance AI System is live on AWS!")
            print(f"🌐 API Endpoint: {api_url}/career-guidance")
            print("📚 Use the API URL in your Streamlit app for production deployment")
        else:
            print("\n⚠️ Deployment completed but tests failed")
            print("Check the Lambda function logs for debugging")
        
        # Cleanup
        if os.path.exists(orchestrator_zip):
            os.remove(orchestrator_zip)
        
        return test_success

def main():
    """Main deployment function"""
    print("AWS Career Guidance AI System - Production Deployment")
    print("=" * 60)
    
    # Check AWS credentials
    try:
        boto3.client('sts').get_caller_identity()
        print("✅ AWS credentials verified")
    except Exception as e:
        print(f"❌ AWS credentials not configured: {e}")
        print("Please configure AWS credentials using 'aws configure'")
        return
    
    # Deploy system
    deployer = AWSDeployer()
    success = deployer.deploy_system()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        print("Your Career Guidance AI System is now live on AWS!")
    else:
        print("\n❌ Deployment failed. Check the errors above.")

if __name__ == "__main__":
    main()

