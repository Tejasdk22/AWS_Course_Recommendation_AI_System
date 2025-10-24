#!/usr/bin/env python3
"""
Test script for AWS Career Guidance AI System
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from career_guidance_system import CareerGuidanceSystem


async def test_system():
    """Test the career guidance system with sample queries."""
    print("🧪 Testing AWS Career Guidance AI System")
    print("=" * 50)
    
    # Initialize the system
    system = CareerGuidanceSystem()
    
    # Test queries
    test_queries = [
        "I want to become a data scientist. What should I learn?",
        "What are the most in-demand skills in tech right now?",
        "I'm a beginner in programming. What projects should I start with?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query {i}: {query}")
        print("-" * 50)
        
        try:
            # Process the query
            response = await system.process_query(query)
            
            print(f"✅ Response generated successfully")
            print(f"Session ID: {response.session_id}")
            print(f"Response length: {len(response.unified_response)} characters")
            print(f"Timestamp: {response.timestamp}")
            
            # Show a preview of the response
            preview = response.unified_response[:200] + "..." if len(response.unified_response) > 200 else response.unified_response
            print(f"Preview: {preview}")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
    
    # Test system status
    print(f"\n📊 System Status:")
    print("-" * 30)
    try:
        status = system.get_system_status()
        print(f"Status: {status['status']}")
        print(f"Active Sessions: {status['active_sessions']}")
        print(f"Agents Initialized: {status['agents_initialized']}")
        print(f"Cache Enabled: {status['cache_enabled']}")
    except Exception as e:
        print(f"❌ Status check failed: {e}")
    
    # Test health check
    print(f"\n🏥 Health Check:")
    print("-" * 30)
    try:
        health = await system.health_check()
        print(f"Overall Status: {health['overall_status']}")
        for agent_name, agent_status in health['agents'].items():
            print(f"{agent_name}: {agent_status['status']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    print(f"\n✅ Testing completed at {datetime.now().isoformat()}")


async def test_individual_agents():
    """Test individual agents separately."""
    print("\n🤖 Testing Individual Agents")
    print("=" * 50)
    
    from agents import JobMarketAgent, CourseCatalogAgent, CareerMatchingAgent, ProjectAdvisorAgent
    
    agents = {
        "JobMarketAgent": JobMarketAgent(),
        "CourseCatalogAgent": CourseCatalogAgent(),
        "CareerMatchingAgent": CareerMatchingAgent(),
        "ProjectAdvisorAgent": ProjectAdvisorAgent()
    }
    
    for agent_name, agent in agents.items():
        print(f"\n🔍 Testing {agent_name}")
        print("-" * 30)
        
        try:
            # Test basic functionality
            print(f"Agent Name: {agent.agent_name}")
            print(f"Logger: {'✅' if agent.logger else '❌'}")
            print(f"Bedrock Client: {'✅' if agent.bedrock_client else '❌'}")
            
            # Test data loading/saving
            test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
            save_result = agent.save_data(test_data, f"test_{agent_name.lower()}.json")
            print(f"Save Data: {'✅' if save_result else '❌'}")
            
            load_result = agent.load_data(f"test_{agent_name.lower()}.json")
            print(f"Load Data: {'✅' if load_result else '❌'}")
            
        except Exception as e:
            print(f"❌ Agent test failed: {e}")


if __name__ == "__main__":
    print("Starting AWS Career Guidance AI System Tests")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_system())
    asyncio.run(test_individual_agents())
    
    print("\n🎉 All tests completed!")
