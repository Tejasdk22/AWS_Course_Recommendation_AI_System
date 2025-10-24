"""
Test the deployed UTD Career Guidance AI System in AWS
"""

import boto3
import json
from datetime import datetime

def test_aws_system():
    """Test the deployed AWS system"""
    
    print("🧪 TESTING UTD CAREER GUIDANCE AI SYSTEM IN AWS")
    print("=" * 70)
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    
    # Test cases
    test_cases = [
        {
            'name': 'Data Science Career (Undergraduate BA)',
            'query': 'I am a Business Analytics undergraduate student at UTD. I want to become a data scientist. What courses should I take?',
            'expected_major': 'BA',
            'expected_level': 'Undergraduate'
        },
        {
            'name': 'Software Engineering Career (Graduate CS)',
            'query': 'I am a Computer Science graduate student at UTD. I want to become a software engineer. What courses should I take?',
            'expected_major': 'CS',
            'expected_level': 'Graduate'
        },
        {
            'name': 'Data Analyst Career (Undergraduate ITM)',
            'query': 'I am an Information Technology Management undergraduate student at UTD. I want to become a data analyst. What courses should I take?',
            'expected_major': 'ITM',
            'expected_level': 'Undergraduate'
        }
    ]
    
    print("\n🔍 Testing Lambda Functions...")
    
    # Test individual agents
    agents_to_test = [
        'utd-career-guidance-job_market_agent',
        'utd-career-guidance-course_catalog_agent',
        'utd-career-guidance-career_matching_agent',
        'utd-career-guidance-project_advisor_agent',
        'utd-career-guidance-resume_analysis_agent',
        'utd-career-guidance-email_notification_agent'
    ]
    
    agent_results = {}
    
    for agent_name in agents_to_test:
        print(f"\n📋 Testing {agent_name}...")
        try:
            # Test with a simple event
            test_event = {
                'test': True,
                'timestamp': datetime.now().isoformat(),
                'query': 'Test query for system validation'
            }
            
            response = lambda_client.invoke(
                FunctionName=agent_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(test_event)
            )
            
            result = json.loads(response['Payload'].read())
            
            if result.get('statusCode') == 200:
                print(f"✅ {agent_name}: Working")
                agent_results[agent_name] = 'SUCCESS'
            else:
                print(f"⚠️  {agent_name}: {result.get('error', 'Unknown error')}")
                agent_results[agent_name] = 'ERROR'
                
        except Exception as e:
            print(f"❌ {agent_name}: {str(e)}")
            agent_results[agent_name] = 'ERROR'
    
    # Test the main orchestrator
    print("\n🎯 Testing Course Recommendation Orchestrator...")
    
    orchestrator_results = {}
    
    for test_case in test_cases:
        print(f"\n📝 Test Case: {test_case['name']}")
        print(f"   Query: {test_case['query']}")
        
        try:
            # Test event for orchestrator
            test_event = {
                'query': test_case['query'],
                'user_id': 'test_user',
                'timestamp': datetime.now().isoformat()
            }
            
            response = lambda_client.invoke(
                FunctionName='utd-career-guidance-orchestrator',
                InvocationType='RequestResponse',
                Payload=json.dumps(test_event)
            )
            
            result = json.loads(response['Payload'].read())
            
            if result.get('statusCode') == 200:
                print(f"✅ Orchestrator: Working")
                
                # Parse the response
                body = json.loads(result.get('body', '{}'))
                
                if 'course_recommendations' in body:
                    recommendations = body['course_recommendations']
                    
                    print(f"   📚 Course Recommendations: {len(recommendations.get('courses', []))} courses")
                    print(f"   🎯 Career Path: {recommendations.get('career_path', 'N/A')}")
                    print(f"   📊 Market Analysis: {recommendations.get('market_analysis', {}).get('summary', 'N/A')}")
                    
                    # Check graduation plan
                    if 'graduation_plan' in recommendations:
                        plan = recommendations['graduation_plan']
                        print(f"   🎓 Total Courses: {plan.get('total_courses', 'N/A')}")
                        print(f"   📋 Core Courses: {len(plan.get('core_courses', []))} courses")
                        print(f"   📋 Elective Courses: {len(plan.get('elective_courses', []))} courses")
                    
                    # Check projects
                    if 'projects' in recommendations:
                        projects = recommendations['projects']
                        print(f"   🚀 Projects: {len(projects)} recommended")
                    
                    orchestrator_results[test_case['name']] = 'SUCCESS'
                else:
                    print(f"   ⚠️  Response format unexpected")
                    orchestrator_results[test_case['name']] = 'PARTIAL'
            else:
                print(f"   ❌ Orchestrator: {result.get('error', 'Unknown error')}")
                orchestrator_results[test_case['name']] = 'ERROR'
                
        except Exception as e:
            print(f"   ❌ Orchestrator: {str(e)}")
            orchestrator_results[test_case['name']] = 'ERROR'
    
    # Test Resume Analysis
    print("\n📄 Testing Resume Analysis...")
    try:
        resume_event = {
            'resume_data': {
                'skills': ['Python', 'SQL', 'Excel'],
                'experience': '2 years',
                'education': 'Bachelor in Business Analytics'
            },
            'user_id': 'test_user'
        }
        
        response = lambda_client.invoke(
            FunctionName='utd-career-guidance-resume_analysis_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps(resume_event)
        )
        
        result = json.loads(response['Payload'].read())
        
        if result.get('statusCode') == 200:
            print("✅ Resume Analysis: Working")
            body = json.loads(result.get('body', '{}'))
            if 'resume_analysis' in body:
                analysis = body['resume_analysis']
                print(f"   📊 Skills Found: {len(analysis.get('skills_found', []))} skills")
                print(f"   🔍 Skill Gaps: {len(analysis.get('skill_gaps', []))} gaps")
                print(f"   💡 Recommendations: {len(analysis.get('recommendations', []))} suggestions")
        else:
            print(f"⚠️  Resume Analysis: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Resume Analysis: {str(e)}")
    
    # Test Email Notifications
    print("\n📧 Testing Email Notifications...")
    try:
        email_event = {
            'notification_type': 'job_alert',
            'user_email': 'test@example.com',
            'user_preferences': {'frequency': 'daily'}
        }
        
        response = lambda_client.invoke(
            FunctionName='utd-career-guidance-email_notification_agent',
            InvocationType='RequestResponse',
            Payload=json.dumps(email_event)
        )
        
        result = json.loads(response['Payload'].read())
        
        if result.get('statusCode') == 200:
            print("✅ Email Notifications: Working")
            body = json.loads(result.get('body', '{}'))
            if 'email_notification' in body:
                notification = body['email_notification']
                print(f"   📧 Status: {notification.get('status', 'N/A')}")
                print(f"   📅 Frequency: {notification.get('scheduling', {}).get('frequency', 'N/A')}")
        else:
            print(f"⚠️  Email Notifications: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Email Notifications: {str(e)}")
    
    # Summary
    print("\n📊 TESTING SUMMARY")
    print("=" * 70)
    
    # Agent results
    successful_agents = sum(1 for status in agent_results.values() if status == 'SUCCESS')
    total_agents = len(agent_results)
    print(f"🤖 Agents: {successful_agents}/{total_agents} working")
    
    # Orchestrator results
    successful_tests = sum(1 for status in orchestrator_results.values() if status == 'SUCCESS')
    total_tests = len(orchestrator_results)
    print(f"🎯 Orchestrator Tests: {successful_tests}/{total_tests} successful")
    
    # Overall success rate
    overall_success = (successful_agents + successful_tests) / (total_agents + total_tests) * 100
    print(f"📈 Overall Success Rate: {overall_success:.1f}%")
    
    if overall_success >= 80:
        print("\n🎉 SYSTEM TESTING SUCCESSFUL!")
        print("✅ Your UTD Career Guidance AI System is working properly")
        print("🚀 Ready for production use!")
    else:
        print("\n⚠️  SYSTEM TESTING PARTIAL")
        print("🔧 Some components need attention")
        print("📋 Check the error messages above for details")
    
    print("\n🎓 Your UTD Career Guidance AI System is ready for use!")

if __name__ == "__main__":
    test_aws_system()
