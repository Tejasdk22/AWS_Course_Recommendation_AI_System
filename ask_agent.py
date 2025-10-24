#!/usr/bin/env python3
"""
Simple Ask Agent - One-liner prompt input
"""

import boto3
import json
import sys

def ask_agent(question):
    """Ask the agent a single question"""
    
    lambda_client = boto3.client('lambda')
    
    print(f"🤖 Asking: '{question}'")
    print("⏳ Agents are working...")
    
    try:
        response = lambda_client.invoke(
            FunctionName='utd-career-guidance-orchestrator',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query': question,
                'sessionId': 'ask-agent'
            })
        )
        
        result = json.loads(response['Payload'].read())
        
        if result['statusCode'] == 200:
            body = json.loads(result['body'])
            
            # Handle both old and new response formats
            if 'career_guidance' in body:
                # Old format
                summary = body['career_guidance']['summary']
                print("\n✅ AGENT RESPONSE:")
                print("=" * 50)
                print(f"🎯 Career Path: {summary['career_path']}")
                print(f"📚 Key Skills: {summary['key_skills_needed']}")
                print(f"🎓 Courses: {summary['recommended_utd_courses']}")
                print(f"🚀 Next Steps: {summary['next_steps']}")
                print("=" * 50)
            elif 'course_recommendations' in body:
                # New course recommendation format
                recommendations = body['course_recommendations']
                print("\n✅ COURSE RECOMMENDATIONS:")
                print("=" * 50)
                print(f"🎯 Career Path: {recommendations['career_path']}")
                print(f"📚 Key Skills: {recommendations['key_skills_needed']}")
                
                if 'graduation_plan' in recommendations:
                    plan = recommendations['graduation_plan']
                    print(f"\\n🎓 GRADUATION PLAN:")
                    if 'total_credits' in plan:
                        print(f"   Total Credits: {plan['total_credits']}")
                        print(f"   Total Courses: {plan['total_courses']}")
                        print(f"   Core Curriculum: {plan['core_curriculum']}")
                        print(f"   Major Courses: {plan['major_courses']}")
                        print(f"   Electives: {plan['electives']}")
                        print(f"   Requirements: {plan['graduation_requirements']}")
                    else:
                        print(f"   Total Courses: {plan['total_courses']}")
                        print(f"   Core Courses: {plan['core_courses']} (Required)")
                        print(f"   Elective Courses: {plan['elective_courses']} (Chosen)")
                        print(f"   Core Completion: {plan['core_completion']}")
                        print(f"   Elective Focus: {plan['elective_focus']}")
                
                if recommendations.get('student_type') == 'Undergraduate':
                    if 'core_curriculum_courses' in recommendations:
                        print(f"\\n📚 CORE CURRICULUM (14 courses):")
                        for i, course in enumerate(recommendations['core_curriculum_courses'], 1):
                            print(f"   {i}. {course}")
                    
                    if 'major_courses' in recommendations:
                        print(f"\\n🎯 MAJOR COURSES (14 courses):")
                        for i, course in enumerate(recommendations['major_courses'], 1):
                            print(f"   {i}. {course}")
                    
                    if 'free_electives' in recommendations:
                        print(f"\\n📖 FREE ELECTIVES (10-15 courses):")
                        for i, course in enumerate(recommendations['free_electives'], 1):
                            print(f"   {i}. {course}")
                else:
                    if 'core_courses' in recommendations:
                        print(f"\\n📚 CORE COURSES (6 Required):")
                        for i, course in enumerate(recommendations['core_courses'], 1):
                            print(f"   {i}. {course}")
                    
                    if 'elective_courses' in recommendations:
                        print(f"\\n🎯 ELECTIVE COURSES (6 Chosen):")
                        for i, course in enumerate(recommendations['elective_courses'], 1):
                            print(f"   {i}. {course}")
                
                print(f"\\n📋 Course Sequence: {recommendations['course_sequence']}")
                print(f"📝 Prerequisites: {recommendations['prerequisites']}")
                print(f"🚀 Next Steps: {recommendations['next_steps']}")
                print("=" * 50)
            else:
                print("\n✅ AGENT RESPONSE:")
                print("=" * 50)
                print(f"Response: {body}")
                print("=" * 50)
            
        else:
            print(f"❌ ERROR: {result}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        ask_agent(question)
    else:
        print("Usage: python3 ask_agent.py 'Your question here'")
        print("Example: python3 ask_agent.py 'I want to become a data scientist'")
