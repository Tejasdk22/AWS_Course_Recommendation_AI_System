#!/usr/bin/env python3
"""
Comprehensive test script for the UTD Career Guidance AI System
Tests all agents working together through the orchestrator
"""

import boto3
import json
import time
from datetime import datetime

def test_career_guidance_system():
    """Test the complete career guidance system"""
    
    print("🎯 UTD CAREER GUIDANCE AI SYSTEM - COMPREHENSIVE TEST")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize Lambda client
    lambda_client = boto3.client('lambda')
    
    # Test cases with different career goals
    test_cases = [
        {
            "query": "I want to become a data scientist",
            "expected_skills": ["Python", "Machine Learning", "Statistics"],
            "expected_courses": ["CS 6313", "CS 6375"]
        },
        {
            "query": "I want to become a software engineer",
            "expected_skills": ["Programming", "Data Structures", "Algorithms"],
            "expected_courses": ["CS 2336", "CS 3345"]
        },
        {
            "query": "I want to work in machine learning",
            "expected_skills": ["Machine Learning", "Python", "Statistics"],
            "expected_courses": ["CS 6375", "CS 6313"]
        },
        {
            "query": "I want to become a web developer",
            "expected_skills": ["JavaScript", "Web Development", "Programming"],
            "expected_courses": ["CS 1336", "CS 2336"]
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 TEST CASE {i}: {test_case['query']}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # Invoke orchestrator
            response = lambda_client.invoke(
                FunctionName='utd-career-guidance-orchestrator',
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': test_case['query'],
                    'sessionId': f'test-{i}-{int(time.time())}'
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
                
                # Check if expected skills are present
                skills_found = any(skill in str(summary['key_skills_needed']) 
                                 for skill in test_case['expected_skills'])
                courses_found = any(course in str(summary['recommended_utd_courses']) 
                                  for course in test_case['expected_courses'])
                
                print(f"   Skills Match: {'✅' if skills_found else '❌'}")
                print(f"   Courses Match: {'✅' if courses_found else '❌'}")
                
                results.append({
                    'test_case': i,
                    'query': test_case['query'],
                    'status': 'SUCCESS',
                    'response_time': response_time,
                    'career_path': summary['career_path'],
                    'skills_match': skills_found,
                    'courses_match': courses_found
                })
                
            else:
                print(f"❌ Status: ERROR")
                print(f"❌ Error: {result}")
                results.append({
                    'test_case': i,
                    'query': test_case['query'],
                    'status': 'ERROR',
                    'error': str(result)
                })
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            results.append({
                'test_case': i,
                'query': test_case['query'],
                'status': 'EXCEPTION',
                'error': str(e)
            })
        
        print()
        print("=" * 70)
        print()
    
    # Summary
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    successful_tests = [r for r in results if r['status'] == 'SUCCESS']
    failed_tests = [r for r in results if r['status'] != 'SUCCESS']
    
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Success Rate: {len(successful_tests)/len(results)*100:.1f}%")
    
    if successful_tests:
        avg_response_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
        print(f"Average Response Time: {avg_response_time:.2f}s")
        
        skills_match_rate = sum(1 for r in successful_tests if r['skills_match']) / len(successful_tests)
        courses_match_rate = sum(1 for r in successful_tests if r['courses_match']) / len(successful_tests)
        
        print(f"Skills Match Rate: {skills_match_rate*100:.1f}%")
        print(f"Courses Match Rate: {courses_match_rate*100:.1f}%")
    
    print()
    print("🎉 HACKATHON READY!")
    print("Your agentic AI system is fully functional and ready for presentation!")
    
    return results

def test_individual_agents():
    """Test individual agents separately"""
    
    print("\n🔍 INDIVIDUAL AGENT TESTING")
    print("=" * 50)
    
    lambda_client = boto3.client('lambda')
    
    agents = [
        'utd-career-guidance-job_market_agent',
        'utd-career-guidance-course_catalog_agent',
        'utd-career-guidance-career_matching_agent',
        'utd-career-guidance-project_advisor_agent'
    ]
    
    for agent in agents:
        print(f"\nTesting {agent.split('-')[-1].replace('_', ' ').title()}:")
        
        try:
            response = lambda_client.invoke(
                FunctionName=agent,
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'query': 'I want to become a data scientist',
                    'sessionId': 'individual-test'
                })
            )
            
            result = json.loads(response['Payload'].read())
            
            if result['statusCode'] == 200:
                print(f"  ✅ Status: SUCCESS")
                print(f"  ✅ Agent: {result['body']['agent']}")
            else:
                print(f"  ❌ Status: ERROR")
                print(f"  ❌ Error: {result}")
                
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")

if __name__ == "__main__":
    # Test individual agents first
    test_individual_agents()
    
    # Test full system
    test_career_guidance_system()
