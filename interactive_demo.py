#!/usr/bin/env python3
"""
Interactive Demo - Manual Prompt Input
You can type prompts and see agent responses in real-time
"""

import boto3
import json
import time
from datetime import datetime

def interactive_demo():
    """Interactive demo where you can input prompts manually"""
    
    print("🎯 UTD CAREER GUIDANCE AI SYSTEM - INTERACTIVE DEMO")
    print("=" * 70)
    print("Type your career questions and see the agents respond!")
    print("Type 'quit' or 'exit' to stop the demo")
    print("=" * 70)
    
    # Initialize Lambda client
    lambda_client = boto3.client('lambda')
    
    # Demo counter
    demo_count = 0
    
    while True:
        print(f"\n📝 DEMO #{demo_count + 1}")
        print("-" * 30)
        
        # Get user input
        try:
            user_prompt = input("Enter your career question: ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Demo ended by user. Goodbye!")
            break
        
        # Check for exit commands
        if user_prompt.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Demo ended. Goodbye!")
            break
        
        if not user_prompt:
            print("❌ Please enter a valid question.")
            continue
        
        demo_count += 1
        
        # Show processing
        print(f"\n🤖 Processing: '{user_prompt}'")
        print("⏳ Agents are working...")
        
        start_time = time.time()
        
        try:
            # Call the orchestrator
            response = lambda_client.invoke(
                FunctionName='utd-career-guidance-orchestrator',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': user_prompt,
                    'sessionId': f'interactive-demo-{demo_count}'
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
                
                # Display results
                print(f"\n✅ SUCCESS! ({response_time}s)")
                print("=" * 50)
                print(f"🎯 CAREER PATH: {summary['career_path']}")
                print("=" * 50)
                
                print(f"\n📚 KEY SKILLS NEEDED:")
                for i, skill in enumerate(summary['key_skills_needed'], 1):
                    print(f"   {i}. {skill}")
                
                print(f"\n🎓 RECOMMENDED UTD COURSES:")
                for i, course in enumerate(summary['recommended_utd_courses'], 1):
                    print(f"   {i}. {course}")
                
                print(f"\n🚀 NEXT STEPS:")
                for i, step in enumerate(summary['next_steps'], 1):
                    print(f"   {i}. {step}")
                
                print(f"\n🤖 AGENT COORDINATION:")
                print(f"   • Agents Involved: {coordination['agents_involved']}")
                print(f"   • Coordination: {coordination['coordination_successful']}")
                print(f"   • Processing Time: {coordination['processing_time']}")
                
                print("\n" + "=" * 50)
                print("🎉 This demonstrates autonomous agents working together!")
                
            else:
                print(f"\n❌ ERROR: {result}")
                
        except Exception as e:
            print(f"\n❌ EXCEPTION: {str(e)}")
        
        print("\n" + "=" * 70)

def quick_demo():
    """Quick demo with predefined questions"""
    
    print("🎯 UTD CAREER GUIDANCE AI SYSTEM - QUICK DEMO")
    print("=" * 70)
    
    # Predefined demo questions
    demo_questions = [
        "I want to become a data scientist",
        "I want to become a software engineer",
        "I want to work in cybersecurity",
        "I want to become a machine learning engineer"
    ]
    
    lambda_client = boto3.client('lambda')
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n📝 DEMO #{i}: {question}")
        print("-" * 50)
        
        print("⏳ Agents are working...")
        start_time = time.time()
        
        try:
            response = lambda_client.invoke(
                FunctionName='utd-career-guidance-orchestrator',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': question,
                    'sessionId': f'quick-demo-{i}'
                })
            )
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                body = json.loads(result['body'])
                summary = body['career_guidance']['summary']
                
                print(f"✅ SUCCESS! ({response_time}s)")
                print(f"🎯 Career Path: {summary['career_path']}")
                print(f"📚 Key Skills: {summary['key_skills_needed'][:3]}...")
                print(f"🎓 Courses: {summary['recommended_utd_courses'][:2]}...")
                
            else:
                print(f"❌ ERROR: {result}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
        
        print("=" * 70)
    
    print("\n🎉 Quick demo complete!")

def main():
    """Main function with menu"""
    
    print("🎯 UTD CAREER GUIDANCE AI SYSTEM")
    print("=" * 50)
    print("Choose demo mode:")
    print("1. Interactive Demo (Type your own questions)")
    print("2. Quick Demo (Predefined questions)")
    print("3. Exit")
    print("=" * 50)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                interactive_demo()
                break
            elif choice == '2':
                quick_demo()
                break
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo ended by user. Goodbye!")
            break

if __name__ == "__main__":
    main()
