#!/usr/bin/env python3
"""
Test script for Amazon Titan model in AWS Bedrock
"""

import os
import boto3
import json
from dotenv import load_dotenv

def test_titan_model():
    """Test Amazon Titan model with AWS Bedrock."""
    print("🤖 Testing Amazon Titan Model")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    model_id = os.getenv('BEDROCK_MODEL_ID', 'amazon.titan-text-express-v1')
    
    print(f"Region: {aws_region}")
    print(f"Model: {model_id}")
    
    try:
        # Initialize Bedrock client
        bedrock_client = boto3.client('bedrock-runtime', region_name=aws_region)
        
        # Test prompt
        test_prompt = "What are the key skills needed to become a data scientist? Please provide a brief overview."
        
        print(f"\n📝 Test Prompt: {test_prompt}")
        print("\n🔄 Calling Amazon Titan...")
        
        # Call Amazon Titan model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "inputText": test_prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 500,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }),
            contentType="application/json"
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        output_text = response_body.get('results', [{}])[0].get('outputText', 'No response generated')
        
        print("\n✅ Amazon Titan Response:")
        print("-" * 40)
        print(output_text)
        print("-" * 40)
        
        # Check response metadata
        if 'results' in response_body and len(response_body['results']) > 0:
            result = response_body['results'][0]
            print(f"\n📊 Response Metadata:")
            print(f"Token Count: {result.get('tokenCount', 'N/A')}")
            print(f"Finish Reason: {result.get('finishReason', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing Amazon Titan: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your AWS credentials in .env file")
        print("2. Ensure you have Bedrock access enabled")
        print("3. Verify the model ID is correct")
        print("4. Check your IAM permissions")
        return False

def test_available_models():
    """Test listing available models."""
    print("\n🔍 Testing Available Models")
    print("=" * 40)
    
    try:
        aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        bedrock_client = boto3.client('bedrock', region_name=aws_region)
        
        # List foundation models
        response = bedrock_client.list_foundation_models()
        
        # Filter for Amazon Titan models
        titan_models = [model for model in response['modelSummaries'] 
                       if 'amazon.titan' in model['modelId']]
        
        print(f"Found {len(titan_models)} Amazon Titan models:")
        for model in titan_models:
            print(f"  - {model['modelId']}")
            print(f"    Provider: {model['providerName']}")
            print(f"    Status: {model['modelLifecycle']['status']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

if __name__ == "__main__":
    print("Amazon Titan Model Test for Career Guidance AI System")
    print("=" * 60)
    
    # Test available models
    models_ok = test_available_models()
    
    # Test Titan model
    titan_ok = test_titan_model()
    
    if models_ok and titan_ok:
        print("\n🎉 All tests passed! Amazon Titan is working correctly.")
        print("Your Career Guidance AI System is ready to use!")
    else:
        print("\n❌ Some tests failed. Please check the configuration.")