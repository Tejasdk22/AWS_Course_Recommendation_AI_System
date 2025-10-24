#!/usr/bin/env python3
"""
Check for existing IAM roles that can be used for Lambda functions
"""

import boto3
import json

def check_existing_roles():
    """Check for existing IAM roles that can be used"""
    iam = boto3.client('iam')
    
    print("🔍 Checking for existing IAM roles...")
    
    try:
        # List all roles
        response = iam.list_roles()
        
        print(f"Found {len(response['Roles'])} IAM roles:")
        
        lambda_roles = []
        for role in response['Roles']:
            role_name = role['RoleName']
            role_arn = role['Arn']
            
            # Check if it's a Lambda execution role
            if 'lambda' in role_name.lower() or 'execution' in role_name.lower():
                lambda_roles.append({
                    'name': role_name,
                    'arn': role_arn
                })
                print(f"✅ Potential Lambda role: {role_name}")
            else:
                print(f"  - {role_name}")
        
        if lambda_roles:
            print(f"\n🎯 Found {len(lambda_roles)} potential Lambda execution roles:")
            for role in lambda_roles:
                print(f"  - {role['name']}: {role['arn']}")
            return lambda_roles[0]['arn']  # Return first one
        else:
            print("\n❌ No existing Lambda execution roles found")
            return None
            
    except Exception as e:
        print(f"❌ Error checking roles: {e}")
        return None

def check_lambda_permissions():
    """Check if we can create Lambda functions"""
    lambda_client = boto3.client('lambda')
    
    print("\n🔍 Checking Lambda permissions...")
    
    try:
        # Try to list existing functions
        response = lambda_client.list_functions()
        print(f"✅ Can access Lambda - found {len(response['Functions'])} existing functions")
        return True
    except Exception as e:
        print(f"❌ Cannot access Lambda: {e}")
        return False

def check_bedrock_permissions():
    """Check Bedrock permissions"""
    bedrock = boto3.client('bedrock')
    
    print("\n🔍 Checking Bedrock permissions...")
    
    try:
        # Try to list foundation models
        response = bedrock.list_foundation_models()
        print(f"✅ Can access Bedrock - found {len(response['modelSummaries'])} models")
        return True
    except Exception as e:
        print(f"❌ Cannot access Bedrock: {e}")
        return False

def main():
    """Main function to check permissions"""
    print("🚀 AWS Permissions Check for Hackathon Deployment")
    print("=" * 60)
    
    # Check existing roles
    lambda_role = check_existing_roles()
    
    # Check Lambda permissions
    lambda_ok = check_lambda_permissions()
    
    # Check Bedrock permissions
    bedrock_ok = check_bedrock_permissions()
    
    print("\n📋 Summary:")
    print("=" * 30)
    print(f"Lambda Role Available: {'✅ Yes' if lambda_role else '❌ No'}")
    print(f"Lambda Access: {'✅ Yes' if lambda_ok else '❌ No'}")
    print(f"Bedrock Access: {'✅ Yes' if bedrock_ok else '❌ No'}")
    
    if lambda_role and lambda_ok and bedrock_ok:
        print("\n🎉 Ready for AWS deployment!")
        print(f"Using Lambda role: {lambda_role}")
        return lambda_role
    else:
        print("\n❌ Need additional permissions for AWS deployment")
        print("Required: IAMFullAccess, AWSLambdaFullAccess, AmazonBedrockFullAccess")
        return None

if __name__ == "__main__":
    main()
