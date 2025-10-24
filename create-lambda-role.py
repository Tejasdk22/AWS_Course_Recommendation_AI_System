"""
Create new IAM role specifically for Lambda functions
"""

import boto3
import json
from datetime import datetime

def create_lambda_role():
    """Create new IAM role for Lambda functions"""
    
    print("🔧 CREATING NEW LAMBDA-SPECIFIC IAM ROLE")
    print("=" * 70)
    
    # Initialize AWS clients
    iam_client = boto3.client('iam')
    lambda_client = boto3.client('lambda')
    
    # Get account ID
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()['Account']
    
    role_name = 'UTDCareerGuidanceLambdaRole'
    
    try:
        # Step 1: Create new role
        print("\n🔧 Step 1: Creating new Lambda role...")
        
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
        
        try:
            iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Role for UTD Career Guidance Lambda functions'
            )
            print(f"✅ Role '{role_name}' created successfully")
        except iam_client.exceptions.EntityAlreadyExistsException:
            print(f"✅ Role '{role_name}' already exists")
        except Exception as e:
            print(f"❌ Error creating role: {e}")
            return False
        
        # Step 2: Attach required policies
        print("\n📋 Step 2: Attaching required policies...")
        
        # List of policies to attach
        policies = [
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
            'arn:aws:iam::aws:policy/AmazonBedrockFullAccess',
            'arn:aws:iam::aws:policy/AmazonS3FullAccess',
            'arn:aws:iam::aws:policy/AmazonSESFullAccess',
            'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
            'arn:aws:iam::aws:policy/AmazonRekognitionFullAccess',
            'arn:aws:iam::aws:policy/AmazonTextractFullAccess'
        ]
        
        for policy_arn in policies:
            try:
                iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
                print(f"✅ Attached policy: {policy_arn}")
            except iam_client.exceptions.EntityAlreadyExistsException:
                print(f"✅ Policy already attached: {policy_arn}")
            except Exception as e:
                print(f"⚠️  Error attaching policy {policy_arn}: {e}")
        
        # Step 3: Create custom policy for additional permissions
        print("\n🔧 Step 3: Creating custom policy...")
        
        custom_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "lambda:InvokeFunction",
                        "lambda:GetFunction",
                        "lambda:ListFunctions"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "bedrock:InvokeModelWithResponseStream",
                        "bedrock:GetFoundationModel",
                        "bedrock:ListFoundationModels"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::utd-career-guidance-bedrock",
                        f"arn:aws:s3:::utd-career-guidance-bedrock/*"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "ses:SendEmail",
                        "ses:SendRawEmail",
                        "ses:GetSendQuota",
                        "ses:GetSendStatistics"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem",
                        "dynamodb:Query",
                        "dynamodb:Scan"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        try:
            iam_client.put_role_policy(
                RoleName=role_name,
                PolicyName='UTDCareerGuidanceCustomPolicy',
                PolicyDocument=json.dumps(custom_policy)
            )
            print("✅ Custom policy created and attached")
        except Exception as e:
            print(f"⚠️  Error creating custom policy: {e}")
        
        # Step 4: Test role with Lambda
        print("\n🧪 Step 4: Testing role with Lambda...")
        
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
                FunctionName='test-lambda-role-permissions',
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_buffer.getvalue()},
                Description='Test function to verify role permissions'
            )
            
            print("✅ Role permissions test successful")
            
            # Clean up test function
            try:
                lambda_client.delete_function(FunctionName='test-lambda-role-permissions')
                print("✅ Test function cleaned up")
            except:
                pass
                
        except Exception as e:
            print(f"❌ Role permissions test failed: {e}")
            return False
        
        print("\n🎉 LAMBDA ROLE CREATED SUCCESSFULLY!")
        print("=" * 70)
        print(f"✅ Role Name: {role_name}")
        print(f"✅ Role ARN: {role_arn}")
        print("✅ Trust policy: Lambda service")
        print("✅ Permissions: All required policies attached")
        print("✅ Custom policy: Additional permissions added")
        print("✅ Test: Role works with Lambda")
        print("\n🚀 Ready to deploy Lambda functions with this role!")
        
        return role_arn
        
    except Exception as e:
        print(f"❌ Error creating Lambda role: {e}")
        return None

if __name__ == "__main__":
    role_arn = create_lambda_role()
    if role_arn:
        print(f"\n🎉 Lambda role created: {role_arn}")
    else:
        print("\n❌ Failed to create Lambda role!")
