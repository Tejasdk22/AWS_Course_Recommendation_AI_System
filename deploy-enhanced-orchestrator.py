"""
Deploy enhanced course orchestrator with detailed course information
"""

import boto3
import json
import zipfile
import os
from datetime import datetime

def deploy_enhanced_orchestrator():
    """Deploy enhanced course orchestrator"""
    
    print("🚀 DEPLOYING ENHANCED COURSE ORCHESTRATOR")
    print("=" * 70)
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    
    # Read the enhanced orchestrator code
    with open('lambda_functions/enhanced_course_orchestrator.py', 'r') as f:
        orchestrator_code = f.read()
    
    # Create deployment package
    print("\n📦 Creating deployment package...")
    
    # Create temporary directory
    temp_dir = "temp_enhanced_orchestrator"
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
    zip_path = "enhanced_orchestrator.zip"
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
    print("\n⚡ Updating Lambda function...")
    try:
        lambda_client.update_function_code(
            FunctionName='utd-career-guidance-orchestrator',
            ZipFile=zip_content
        )
        print("✅ Enhanced orchestrator deployed successfully")
        
        # Clean up zip file
        os.remove(zip_path)
        
        print("\n🎉 ENHANCED ORCHESTRATOR DEPLOYED!")
        print("=" * 70)
        print("✅ Detailed course information included")
        print("✅ Course names and descriptions")
        print("✅ Prerequisites and credit hours")
        print("✅ Skills taught and career relevance")
        print("✅ UTD catalog information integrated")
        print("\n🚀 Ready to test with enhanced course details!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error deploying enhanced orchestrator: {e}")
        return False

if __name__ == "__main__":
    success = deploy_enhanced_orchestrator()
    if success:
        print("\n🎉 Enhanced orchestrator deployed successfully!")
    else:
        print("\n❌ Failed to deploy enhanced orchestrator!")
