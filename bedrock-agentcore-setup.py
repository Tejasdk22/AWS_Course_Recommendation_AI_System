#!/usr/bin/env python3
"""
AWS Bedrock AgentCore Setup Script
Creates autonomous agents for UTD Career Guidance AI System
"""

import boto3
import json
import time
from typing import Dict, Any

class BedrockAgentCoreSetup:
    """Setup AWS Bedrock AgentCore agents for Career Guidance System"""
    
    def __init__(self, region='us-east-1'):
        self.region = region
        self.bedrock_agent = boto3.client('bedrock-agent', region_name=region)
        self.bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        
    def create_job_market_agent(self) -> str:
        """Create JobMarketAgent in Bedrock AgentCore"""
        print("🤖 Creating JobMarketAgent...")
        
        agent_config = {
            "agentName": "JobMarketAgent",
            "description": "Autonomous agent that scrapes job postings from LinkedIn, Indeed, and Glassdoor to analyze market trends, extract skills, and identify salary information",
            "foundationModel": "anthropic.claude-3-sonnet-20240229-v1:0",
            "instruction": """
            You are an autonomous Job Market Analysis Agent. Your responsibilities:
            
            1. AUTONOMOUSLY scrape job postings from LinkedIn, Indeed, and Glassdoor
            2. Extract skills, requirements, and salary information
            3. Identify trending skills and job availability by location
            4. Analyze market demand for specific roles
            5. Provide real-time job market insights
            
            You work independently without human intervention. When given a career query:
            - Automatically search for relevant job postings
            - Extract and analyze skill requirements
            - Identify salary trends and location data
            - Provide comprehensive market analysis
            
            Always provide data-driven insights based on current job postings.
            """,
            "idleSessionTTLInSeconds": 1800,
            "agentResourceRoleArn": self._get_or_create_agent_role(),
            "customerEncryptionKeyArn": None,
            "tags": {
                "Project": "UTD-Career-Guidance",
                "AgentType": "JobMarket"
            }
        }
        
        try:
            response = self.bedrock_agent.create_agent(**agent_config)
            agent_id = response['agent']['agentId']
            print(f"✅ JobMarketAgent created: {agent_id}")
            return agent_id
        except Exception as e:
            print(f"❌ Error creating JobMarketAgent: {e}")
            return None
    
    def create_course_catalog_agent(self) -> str:
        """Create CourseCatalogAgent in Bedrock AgentCore"""
        print("📚 Creating CourseCatalogAgent...")
        
        agent_config = {
            "agentName": "CourseCatalogAgent",
            "description": "Autonomous agent that analyzes UTD course catalog, extracts taught skills and competencies, and maps course relationships",
            "foundationModel": "anthropic.claude-3-sonnet-20240229-v1:0",
            "instruction": """
            You are an autonomous Course Catalog Analysis Agent. Your responsibilities:
            
            1. AUTONOMOUSLY gather UTD course descriptions and prerequisites
            2. Analyze course content to extract taught skills and competencies
            3. Map relationships between different courses and programs
            4. Identify skill gaps in the curriculum
            5. Provide course recommendations based on career goals
            
            You work independently without human intervention. When given a career query:
            - Automatically search relevant UTD courses
            - Extract skills taught in each course
            - Analyze prerequisites and course sequences
            - Map courses to career requirements
            - Provide personalized course recommendations
            
            Always provide specific course codes, descriptions, and skill mappings.
            """,
            "idleSessionTTLInSeconds": 1800,
            "agentResourceRoleArn": self._get_or_create_agent_role(),
            "customerEncryptionKeyArn": None,
            "tags": {
                "Project": "UTD-Career-Guidance",
                "AgentType": "CourseCatalog"
            }
        }
        
        try:
            response = self.bedrock_agent.create_agent(**agent_config)
            agent_id = response['agent']['agentId']
            print(f"✅ CourseCatalogAgent created: {agent_id}")
            return agent_id
        except Exception as e:
            print(f"❌ Error creating CourseCatalogAgent: {e}")
            return None
    
    def create_career_matching_agent(self) -> str:
        """Create CareerMatchingAgent in Bedrock AgentCore"""
        print("🎯 Creating CareerMatchingAgent...")
        
        agent_config = {
            "agentName": "CareerMatchingAgent",
            "description": "Autonomous agent that coordinates with other agents to analyze job requirements vs coursework and generate personalized recommendations",
            "foundationModel": "anthropic.claude-3-sonnet-20240229-v1:0",
            "instruction": """
            You are an autonomous Career Matching Agent. Your responsibilities:
            
            1. AUTONOMOUSLY coordinate with JobMarketAgent and CourseCatalogAgent
            2. Analyze job requirements vs available coursework
            3. Generate personalized course recommendations with explanations
            4. Identify skill gaps and learning paths
            5. Provide comprehensive career guidance
            
            You work independently and coordinate with other agents. When given a career query:
            - Request data from JobMarketAgent about job requirements
            - Request data from CourseCatalogAgent about available courses
            - Analyze the gap between job needs and course offerings
            - Generate personalized recommendations
            - Provide clear explanations and next steps
            
            Always provide actionable, personalized career guidance.
            """,
            "idleSessionTTLInSeconds": 1800,
            "agentResourceRoleArn": self._get_or_create_agent_role(),
            "customerEncryptionKeyArn": None,
            "tags": {
                "Project": "UTD-Career-Guidance",
                "AgentType": "CareerMatching"
            }
        }
        
        try:
            response = self.bedrock_agent.create_agent(**agent_config)
            agent_id = response['agent']['agentId']
            print(f"✅ CareerMatchingAgent created: {agent_id}")
            return agent_id
        except Exception as e:
            print(f"❌ Error creating CareerMatchingAgent: {e}")
            return None
    
    def create_project_advisor_agent(self) -> str:
        """Create ProjectAdvisorAgent in Bedrock AgentCore"""
        print("🛠️ Creating ProjectAdvisorAgent...")
        
        agent_config = {
            "agentName": "ProjectAdvisorAgent",
            "description": "Autonomous agent that suggests specific projects to bridge coursework to job requirements and provides portfolio development guidance",
            "foundationModel": "anthropic.claude-3-sonnet-20240229-v1:0",
            "instruction": """
            You are an autonomous Project Advisor Agent. Your responsibilities:
            
            1. AUTONOMOUSLY suggest specific projects that bridge coursework to job requirements
            2. Recommend technologies and frameworks to learn
            3. Provide portfolio development guidance
            4. Suggest hands-on learning experiences
            5. Guide skill development through practical projects
            
            You work independently without human intervention. When given a career query:
            - Analyze skill gaps from other agents
            - Suggest specific projects to build required skills
            - Recommend technologies and tools to learn
            - Provide step-by-step project guidance
            - Suggest portfolio development strategies
            
            Always provide practical, actionable project recommendations.
            """,
            "idleSessionTTLInSeconds": 1800,
            "agentResourceRoleArn": self._get_or_create_agent_role(),
            "customerEncryptionKeyArn": None,
            "tags": {
                "Project": "UTD-Career-Guidance",
                "AgentType": "ProjectAdvisor"
            }
        }
        
        try:
            response = self.bedrock_agent.create_agent(**agent_config)
            agent_id = response['agent']['agentId']
            print(f"✅ ProjectAdvisorAgent created: {agent_id}")
            return agent_id
        except Exception as e:
            print(f"❌ Error creating ProjectAdvisorAgent: {e}")
            return None
    
    def _get_or_create_agent_role(self) -> str:
        """Get or create IAM role for Bedrock agents"""
        role_name = "BedrockAgentRole"
        
        try:
            # Try to get existing role
            response = self.iam_client.get_role(RoleName=role_name)
            return response['Role']['Arn']
        except:
            # Create new role
            trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "bedrock.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description="Role for Bedrock agents"
            )
            
            # Attach policies
            policies = [
                "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
                "arn:aws:iam::aws:policy/AmazonS3FullAccess",
                "arn:aws:iam::aws:policy/AmazonLambdaFullAccess"
            ]
            
            for policy_arn in policies:
                self.iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
            
            return f"arn:aws:iam::{self.iam_client.get_caller_identity()['Account']}:role/{role_name}"
    
    def create_agent_aliases(self, agent_ids: Dict[str, str]) -> Dict[str, str]:
        """Create aliases for all agents"""
        aliases = {}
        
        for agent_name, agent_id in agent_ids.items():
            if agent_id:
                try:
                    response = self.bedrock_agent.create_agent_alias(
                        agentId=agent_id,
                        agentAliasName="TSTALIASID",
                        description=f"Alias for {agent_name}"
                    )
                    aliases[agent_name] = response['agentAlias']['agentAliasId']
                    print(f"✅ Created alias for {agent_name}: {aliases[agent_name]}")
                except Exception as e:
                    print(f"❌ Error creating alias for {agent_name}: {e}")
        
        return aliases
    
    def setup_all_agents(self) -> Dict[str, Any]:
        """Set up all Bedrock AgentCore agents"""
        print("🚀 Setting up AWS Bedrock AgentCore for UTD Career Guidance AI System")
        print("=" * 80)
        
        # Create all agents
        agent_ids = {
            "JobMarketAgent": self.create_job_market_agent(),
            "CourseCatalogAgent": self.create_course_catalog_agent(),
            "CareerMatchingAgent": self.create_career_matching_agent(),
            "ProjectAdvisorAgent": self.create_project_advisor_agent()
        }
        
        # Create aliases
        aliases = self.create_agent_aliases(agent_ids)
        
        # Save configuration
        config = {
            "agents": agent_ids,
            "aliases": aliases,
            "region": self.region,
            "created_at": time.time()
        }
        
        with open('bedrock-agentcore-config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("\n🎉 All Bedrock AgentCore agents created successfully!")
        print("Configuration saved to: bedrock-agentcore-config.json")
        
        return config

def main():
    """Main setup function"""
    setup = BedrockAgentCoreSetup()
    config = setup.setup_all_agents()
    
    print("\n📋 Next Steps:")
    print("1. Configure agent tools and knowledge bases")
    print("2. Deploy Lambda functions for agent execution")
    print("3. Test agent coordination")
    print("4. Create API Gateway for user interface")

if __name__ == "__main__":
    main()
