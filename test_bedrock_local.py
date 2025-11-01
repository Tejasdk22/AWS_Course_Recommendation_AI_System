#!/usr/bin/env python3
"""
Local Bedrock Test Script
Tests AWS Bedrock functionality without deploying to Streamlit
"""

import os
import json
import boto3
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

class BedrockTester:
    def __init__(self):
        self.region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        self.model_id = os.getenv('BEDROCK_MODEL_ID', 'amazon.titan-text-express-v1')
        
        # Initialize Bedrock client
        try:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.region
            )
            print(f"✅ Bedrock client initialized in {self.region}")
        except Exception as e:
            print(f"❌ Failed to initialize Bedrock client: {e}")
            raise
    
    def test_basic_connection(self):
        """Test basic Bedrock connection"""
        print("\n🔍 Testing Basic Bedrock Connection...")
        
        try:
            # Simple test prompt
            test_prompt = "Hello, can you help me with course recommendations?"
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": test_prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 100,
                        "temperature": 0.7
                    }
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_response = response_body['results'][0]['outputText']
            
            print(f"✅ Bedrock Response: {ai_response[:100]}...")
            return True
            
        except ClientError as e:
            print(f"❌ Bedrock Client Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return False
    
    def test_career_guidance_prompt(self):
        """Test Bedrock with career guidance prompt"""
        print("\n🎯 Testing Career Guidance Prompt...")
        
        try:
            # Career guidance prompt
            prompt = """
            You are a helpful UTD course advisor. A Graduate student in Computer Science wants to become a Data Scientist.
            
            Please provide:
            1. Job market insights for Data Scientist roles
            2. 6 core courses they should take
            3. 6 elective courses they should consider
            4. Career matching analysis
            5. Project suggestions
            
            Format your response clearly with sections and bullet points.
            """
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 2000,
                        "temperature": 0.7
                    }
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_response = response_body['results'][0]['outputText']
            
            print("✅ Career Guidance Response:")
            print("=" * 50)
            print(ai_response)
            print("=" * 50)
            return True
            
        except Exception as e:
            print(f"❌ Career Guidance Test Failed: {e}")
            return False
    
    def test_multi_agent_simulation(self):
        """Test simulating the multi-agent system with Bedrock"""
        print("\n🤖 Testing Multi-Agent Simulation...")
        
        try:
            # Simulate agent responses
            job_market_data = "Data Scientist roles show high demand with $80k-150k salary range"
            course_data = "CS 6301, CS 6304, CS 6307, CS 6313, CS 6314, CS 6320"
            career_match = "Strong alignment with CS background, focus on ML and data skills"
            project_data = "Build ML models, data visualization dashboards, recommendation systems"
            
            # Create unified prompt
            unified_prompt = f"""
            Create a comprehensive career guidance response for a Computer Science Graduate student who wants to become a Data Scientist.
            
            Job Market Data: {job_market_data}
            Available Courses: {course_data}
            Career Matching: {career_match}
            Project Suggestions: {project_data}
            
            Structure your response with:
            - Job Market Analysis
            - Core Courses (6 required)
            - Elective Courses (6 recommended)
            - Career Matching Analysis
            - Project Suggestions
            - Next Steps
            
            Make it personalized and actionable.
            """
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "inputText": unified_prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 3000,
                        "temperature": 0.7
                    }
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_response = response_body['results'][0]['outputText']
            
            print("✅ Multi-Agent Simulation Response:")
            print("=" * 60)
            print(ai_response)
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"❌ Multi-Agent Test Failed: {e}")
            return False
    
    def test_different_majors(self):
        """Test Bedrock with different majors"""
        print("\n📚 Testing Different Majors...")
        
        majors_careers = [
            ("Finance", "Financial Analyst"),
            ("Business Analytics", "Data Scientist"),
            ("Marketing", "Digital Marketing Specialist"),
            ("Computer Science", "Software Engineer")
        ]
        
        for major, career in majors_careers:
            print(f"\n--- Testing {major} → {career} ---")
            
            try:
                prompt = f"""
                Provide career guidance for a Graduate student in {major} who wants to become a {career}.
                
                Include:
                - Job market outlook
                - 6 core courses
                - 6 elective courses
                - Skills needed
                - Career transition advice
                
                Keep response concise but comprehensive.
                """
                
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps({
                        "inputText": prompt,
                        "textGenerationConfig": {
                            "maxTokenCount": 1500,
                            "temperature": 0.7
                        }
                    })
                )
                
                response_body = json.loads(response['body'].read())
                ai_response = response_body['results'][0]['outputText']
                
                print(f"✅ {major} → {career} Response:")
                print(ai_response[:300] + "..." if len(ai_response) > 300 else ai_response)
                
            except Exception as e:
                print(f"❌ {major} → {career} Failed: {e}")
    
    def run_all_tests(self):
        """Run all Bedrock tests"""
        print("🚀 Starting Bedrock Tests...")
        print(f"Region: {self.region}")
        print(f"Model: {self.model_id}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        tests = [
            ("Basic Connection", self.test_basic_connection),
            ("Career Guidance", self.test_career_guidance_prompt),
            ("Multi-Agent Simulation", self.test_multi_agent_simulation),
            ("Different Majors", self.test_different_majors)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            
            try:
                if test_name == "Different Majors":
                    test_func()  # This test doesn't return boolean
                    results[test_name] = "✅ Completed"
                else:
                    success = test_func()
                    results[test_name] = "✅ Passed" if success else "❌ Failed"
            except Exception as e:
                print(f"❌ Test {test_name} crashed: {e}")
                results[test_name] = "❌ Crashed"
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 TEST SUMMARY")
        print(f"{'='*60}")
        
        for test_name, result in results.items():
            print(f"{test_name}: {result}")
        
        passed = sum(1 for result in results.values() if "✅" in result)
        total = len(results)
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Bedrock is working correctly.")
        else:
            print("⚠️ Some tests failed. Check the errors above.")

def main():
    """Main function"""
    print("🎓 UTD Career Guidance - Bedrock Local Test")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("Please set these in your .env file or environment")
        return
    
    try:
        tester = BedrockTester()
        tester.run_all_tests()
    except Exception as e:
        print(f"❌ Failed to initialize tester: {e}")

if __name__ == "__main__":
    main()

