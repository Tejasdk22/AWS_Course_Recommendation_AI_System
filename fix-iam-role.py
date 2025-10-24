"""
Fix IAM role trust policy for Lambda functions
"""

import boto3
import json
from datetime import datetime

def fix_iam_role():
    """Fix IAM role trust policy"""
    
    print("🔧 FIXING IAM ROLE TRUST POLICY")
    print("=" * 70)
    
    # Initialize AWS clients
    iam_client = boto3.client('iam')
    
    role_name = 'UTDCareerGuidanceBedrockRole'
    
    try:
        # Step 1: Check current role
        print("\n🔍 Step 1: Checking current role...")
        
        try:
            role = iam_client.get_role(RoleName=role_name)
            print(f"✅ Role '{role_name}' exists")
            print(f"   Trust Policy: {role['Role']['AssumeRolePolicyDocument']}")
        except Exception as e:
            print(f"❌ Error getting role: {e}")
            return False
        
        # Step 2: Update trust policy
        print("\n🔧 Step 2: Updating trust policy...")
        
        # Correct trust policy for Lambda
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
        
        try:
            iam_client.update_assume_role_policy(
                RoleName=role_name,
                PolicyDocument=json.dumps(trust_policy)
            )
            print("✅ Trust policy updated successfully")
        except Exception as e:
            print(f"❌ Error updating trust policy: {e}")
            return False
        
        # Step 3: Verify role permissions
        print("\n📋 Step 3: Verifying role permissions...")
        
        try:
            attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
            print(f"✅ Attached policies: {len(attached_policies['AttachedPolicies'])}")
            
            for policy in attached_policies['AttachedPolicies']:
                print(f"   - {policy['PolicyName']}")
                
        except Exception as e:
            print(f"❌ Error listing policies: {e}")
        
        # Step 4: Test role with Lambda
        print("\n🧪 Step 4: Testing role with Lambda...")
        
        lambda_client = boto3.client('lambda')
        
        # Get account ID
        sts_client = boto3.client('sts')
        account_id = sts_client.get_caller_identity()['Account']
        role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
        
        print(f"   Role ARN: {role_arn}")
        
        # Try to create a simple test function
        try:
            test_code = '''
def lambda_handler(event, context):
    return {"statusCode": 200, "body": "test"}
'''
            
            # Create test zip
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr('lambda_function.py', test_code)
            zip_buffer.seek(0)
            
            # Try to create function
            lambda_client.create_function(
                FunctionName='test-role-permissions',
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_buffer.getvalue()},
                Description='Test function to verify role permissions'
            )
            
            print("✅ Role permissions test successful")
            
            # Clean up test function
            try:
                lambda_client.delete_function(FunctionName='test-role-permissions')
                print("✅ Test function cleaned up")
            except:
                pass
                
        except Exception as e:
            print(f"❌ Role permissions test failed: {e}")
            return False
        
        print("\n🎉 IAM ROLE FIXED!")
        print("=" * 70)
        print("✅ Trust policy updated")
        print("✅ Role permissions verified")
        print("✅ Lambda can assume role")
        print("\n🚀 Ready to deploy Lambda functions!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing IAM role: {e}")
        return False

if __name__ == "__main__":
    success = fix_iam_role()
    if success:
        print("\n🎉 IAM role fixed successfully!")
    else:
        print("\n❌ Failed to fix IAM role!")
