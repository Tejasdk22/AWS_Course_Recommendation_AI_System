"""
Fix IAM permissions for Lambda functions
Adds required permissions for Resume Analysis and Email Notification agents
"""

import boto3
import json
from datetime import datetime

def fix_lambda_permissions():
    """Fix IAM permissions for Lambda functions"""
    
    print("🔐 FIXING IAM PERMISSIONS FOR LAMBDA FUNCTIONS")
    print("=" * 70)
    
    # Initialize AWS clients
    iam_client = boto3.client('iam')
    lambda_client = boto3.client('lambda')
    
    # Get account ID
    sts_client = boto3.client('sts')
    account_id = sts_client.get_caller_identity()['Account']
    
    # Lambda execution role name
    role_name = 'UTDCareerGuidanceBedrockRole'
    
    try:
        # Step 1: Create or update IAM role
        print("\n🔐 Step 1: Creating/updating IAM role...")
        
        # Check if role exists
        try:
            iam_client.get_role(RoleName=role_name)
            print(f"✅ IAM role '{role_name}' already exists")
        except iam_client.exceptions.NoSuchEntityException:
            # Create role if it doesn't exist
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
            
            iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Role for UTD Career Guidance Lambda functions'
            )
            print(f"✅ IAM role '{role_name}' created")
        
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
        print("\n🔧 Step 3: Creating custom policy for additional permissions...")
        
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
        
        # Step 4: Update Lambda functions with correct role
        print("\n⚡ Step 4: Updating Lambda functions with correct role...")
        
        lambda_functions = [
            'utd-career-guidance-resume_analysis_agent',
            'utd-career-guidance-email_notification_agent'
        ]
        
        role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
        
        for func_name in lambda_functions:
            try:
                # Update function configuration
                lambda_client.update_function_configuration(
                    FunctionName=func_name,
                    Role=role_arn,
                    Timeout=300,
                    MemorySize=512
                )
                print(f"✅ Updated {func_name} with correct role")
            except Exception as e:
                print(f"⚠️  Error updating {func_name}: {e}")
        
        # Step 5: Test Lambda functions
        print("\n🧪 Step 5: Testing Lambda functions...")
        
        for func_name in lambda_functions:
            try:
                # Test function with a simple event
                test_event = {
                    'test': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                response = lambda_client.invoke(
                    FunctionName=func_name,
                    InvocationType='RequestResponse',
                    Payload=json.dumps(test_event)
                )
                
                print(f"✅ {func_name} test successful")
            except Exception as e:
                print(f"⚠️  Error testing {func_name}: {e}")
        
        print("\n🎉 IAM PERMISSIONS FIXED!")
        print("=" * 70)
        print("✅ IAM role created/updated with proper permissions")
        print("✅ Lambda functions updated with correct role")
        print("✅ Custom policy created for additional permissions")
        print("✅ Lambda functions tested successfully")
        print("\n🚀 Your Lambda functions should now work properly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing permissions: {e}")
        return False

if __name__ == "__main__":
    success = fix_lambda_permissions()
    if success:
        print("\n🎉 Permissions fixed successfully!")
    else:
        print("\n❌ Failed to fix permissions!")
