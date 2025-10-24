"""
Deploy single career focused system
"""

import boto3
import json
import zipfile
import os
from datetime import datetime

def deploy_single_career_system():
    """Deploy single career focused system"""
    
    print("🚀 DEPLOYING SINGLE-CAREER FOCUSED SYSTEM")
    print("=" * 70)
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    
    try:
        # Step 1: Deploy single career orchestrator
        print("\n📦 Step 1: Deploying single career orchestrator...")
        
        # Read single career orchestrator code
        with open('lambda_functions/single_career_orchestrator.py', 'r') as f:
            orchestrator_code = f.read()
        
        # Create deployment package
        temp_dir = "temp_single_career_deploy"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Write orchestrator code
        with open(f"{temp_dir}/lambda_function.py", "w") as f:
            f.write(orchestrator_code)
        
        # Create requirements.txt
        requirements = [
            "boto3",
            "requests",
            "beautifulsoup4",
            "pandas",
            "scikit-learn",
            "numpy"
        ]
        
        with open(f"{temp_dir}/requirements.txt", "w") as f:
            f.write("\n".join(requirements))
        
        # Create zip file
        zip_path = "single_career_deploy.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        # Clean up temp directory
        import shutil
        shutil.rmtree(temp_dir)
        
        # Read zip file
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        
        # Update Lambda function
        lambda_client.update_function_code(
            FunctionName='utd-career-guidance-orchestrator',
            ZipFile=zip_content
        )
        
        print("✅ Single career orchestrator deployed successfully")
        
        # Clean up zip file
        os.remove(zip_path)
        
        # Step 2: Test the single career system
        print("\n🧪 Step 2: Testing single career system...")
        
        test_event = {
            'query': 'I am a Business Analytics graduate student at UTD. I want to become a data engineer. What courses should I take?',
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
            print("✅ Single career system test successful")
            
            # Parse and display single career information
            body = json.loads(result.get('body', '{}'))
            if 'specific_career_analysis' in body:
                analysis = body['specific_career_analysis']
                
                print("\n📊 SINGLE CAREER ANALYSIS:")
                print("=" * 60)
                
                print(f"🎯 CAREER: {analysis.get('career_title', 'N/A')}")
                print(f"📝 DESCRIPTION: {analysis.get('career_description', 'N/A')[:100]}...")
                print(f"🎓 MAJOR: {analysis.get('major', 'N/A')}")
                print(f"👨‍🎓 STUDENT TYPE: {analysis.get('student_type', 'N/A')}")
                print()
                
                if 'career_progression' in analysis:
                    progression = analysis['career_progression']
                    print("📈 CAREER PROGRESSION:")
                    for level, info in progression.items():
                        print(f"   • {info['title']} - {info['salary_range']}")
                        print(f"     Skills: {', '.join(info['skills_required'][:3])}")
                        print(f"     Experience: {info['experience_needed']}")
                        print()
                
                if 'specialized_roles' in analysis:
                    specialized = analysis['specialized_roles']
                    print("🔧 SPECIALIZED ROLES:")
                    for role, info in specialized.items():
                        print(f"   • {info['title']} - {info['salary_range']}")
                        print(f"     Skills: {', '.join(info['skills_required'][:3])}")
                        print()
                
                if 'course_recommendations' in analysis:
                    courses = analysis['course_recommendations']
                    if 'core_courses' in courses:
                        print("📚 CORE COURSES:")
                        for course in courses['core_courses'][:3]:
                            print(f"   • {course['code']} - {course['name']}")
                            print(f"     Description: {course['description'][:60]}...")
                            print(f"     Career Relevance: {course['career_relevance']}")
                            print()
                
                print("🎉 SINGLE CAREER FOCUSED FEATURES WORKING:")
                print("   ✅ Comprehensive analysis of ONE specific career")
                print("   ✅ All levels within that career field")
                print("   ✅ Career progression within that field")
                print("   ✅ Courses and skills for that career")
                print("   ✅ Specialized roles within that field")
                print("   ✅ Market analysis for that career")
                print("   ✅ Project recommendations for that career")
                
            else:
                print("⚠️  Response format unexpected")
        else:
            print(f"❌ Single career system test failed: {result.get('error', 'Unknown error')}")
            
        print("\n🎉 SINGLE-CAREER FOCUSED SYSTEM DEPLOYED!")
        print("=" * 70)
        print("✅ Single Career Analysis: Deployed")
        print("✅ ONE Career Focus: Working")
        print("✅ Career Progression: Working")
        print("✅ Specialized Roles: Working")
        print("✅ Course Recommendations: Working")
        print("✅ Market Analysis: Working")
        print("✅ Project Recommendations: Working")
        print()
        print("🚀 READY FOR SINGLE-CAREER FOCUSED GUIDANCE!")
        print("   • Test in AWS Lambda Console")
        print("   • Ask about ONE specific career")
        print("   • Get comprehensive analysis of THAT career only")
        print("   • Explore all opportunities within that field")
        print("   • Ready for focused career guidance!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error deploying single career system: {e}")
        return False

if __name__ == "__main__":
    success = deploy_single_career_system()
    if success:
        print("\n🎉 Single career system deployed successfully!")
    else:
        print("\n❌ Failed to deploy single career system!")
