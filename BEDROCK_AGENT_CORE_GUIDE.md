# 🚀 Bedrock Agent Core Integration Guide

## 📋 Overview

The AWS Career Guidance AI System now supports **Bedrock Agent Core** alongside direct Bedrock runtime, providing enhanced planning, tool orchestration, and intelligent agent capabilities.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                   (Streamlit App)                        │
│                  Agent Core Toggle                       │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP POST + useAgentCore flag
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                         │
│                   (Port 8000)                           │
│   ┌──────────────────────────────────────────────┐      │
│   │     CareerGuidanceSystem (Orchestrator)      │      │
│   │                                                │      │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │      │
│   │  │   Job    │  │  Course  │  │  Career  │   │      │
│   │  │  Market  │  │ Catalog  │  │ Matching │   │      │
│   │  │  Agent   │  │  Agent   │  │  Agent   │   │      │
│   │  └──────────┘  └──────────┘  └──────────┘   │      │
│   │                                                │      │
│   │  ┌──────────┐                                 │      │
│   │  │ Project  │                                 │      │
│   │  │ Advisor  │                                 │      │
│   │  │  Agent   │                                 │      │
│   │  └──────────┘                                 │      │
│   └────────────────────────────────────────────────┘      │
│                      │                                    │
│                      ▼                                    │
│              ┌──────────────┐                           │
│              │ BaseAgent    │                           │
│              │ (Dual Mode)  │                           │
│              └──────┬───────┘                           │
│                     │                                   │
│         ┌───────────┼───────────┐                      │
│         ▼           ▼           ▼                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │
│  │Bedrock Agent│ │Bedrock Agent │ │Bedrock      │     │
│  │Core         │ │Core          │ │Runtime      │     │
│  │(Enhanced)   │ │(Planning)    │ │(Direct)     │     │
│  └─────────────┘ └─────────────┘ └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# AWS Bedrock Agent Core Configuration
USE_BEDROCK_AGENT_CORE=false
BEDROCK_AGENT_ID=ag-xxxxxxxx
BEDROCK_AGENT_ALIAS_ID=ag-alias-xxxxxxxx
```

### Required AWS Permissions

Your IAM role/user needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent",
                "bedrock:ListAgents",
                "bedrock:ListAgentAliases",
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🚀 Usage

### 1. **Streamlit App**

The app now includes an Agent Core toggle:

```python
# Agent Core Toggle
use_agent_core = st.checkbox(
    "Use Bedrock Agent Core",
    value=False,
    help="Enable Bedrock Agent Core for enhanced planning and tool orchestration"
)
```

### 2. **API Endpoint**

The backend API supports the `useAgentCore` parameter:

```bash
curl -X POST http://localhost:8000/api/career-guidance \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I want to become a data scientist",
    "major": "business analytics",
    "studentType": "graduate",
    "useAgentCore": true
  }'
```

### 3. **Programmatic Usage**

```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    async def respond(self, data, query=None):
        # Use Agent Core for enhanced planning
        response = await self.invoke_bedrock(
            prompt="Analyze this data...",
            use_agent_core=True
        )
        return response
```

## 🔄 Dual Mode Operation

### Mode 1: Direct Bedrock Runtime (Default)
- **Use Case**: Standard AI responses
- **Performance**: Fast, direct model invocation
- **Configuration**: `USE_BEDROCK_AGENT_CORE=false`

### Mode 2: Bedrock Agent Core (Enhanced)
- **Use Case**: Complex planning, tool orchestration
- **Performance**: Slower but more intelligent
- **Configuration**: `USE_BEDROCK_AGENT_CORE=true`

## 📊 Features Comparison

| Feature | Direct Bedrock | Agent Core |
|---------|---------------|------------|
| **Planning** | ❌ No planning | ✅ Intelligent planning |
| **Tool Integration** | ❌ Manual | ✅ Automatic |
| **Context Management** | ⚠️ Basic | ✅ Advanced |
| **Error Handling** | ⚠️ Basic | ✅ Robust |
| **Performance** | ✅ Fast | ⚠️ Slower |
| **Cost** | ✅ Lower | ⚠️ Higher |

## 🛠️ Implementation Details

### BaseAgent Enhancement

```python
class BaseAgent:
    def __init__(self):
        # Agent Core configuration
        self.use_agent_core = os.getenv('USE_BEDROCK_AGENT_CORE', 'false').lower() == 'true'
        self.agent_core_available = is_agent_core_available()
    
    async def invoke_bedrock(self, prompt, context=None, use_agent_core=None):
        # Determine whether to use Agent Core
        should_use_agent_core = use_agent_core if use_agent_core is not None else self.use_agent_core
        
        if should_use_agent_core and self.agent_core_available:
            return await self._invoke_agent_core(prompt, context)
        
        return await self._invoke_bedrock_runtime(prompt, context)
```

### Agent Core Wrapper

```python
class BedrockAgentCore:
    async def invoke_agent(self, input_text, session_id=None):
        response = self.client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            inputText=input_text,
            sessionId=session_id
        )
        
        # Process streaming response
        output_text = ""
        for event in response['completion']:
            if 'chunk' in event:
                output_text += event['chunk']['bytes'].decode('utf-8')
        
        return output_text
```

## 🧪 Testing

### 1. **Test Agent Core Availability**

```python
from agents.bedrock_agent_core import is_agent_core_available, get_agent_core_info

# Check if Agent Core is configured
if is_agent_core_available():
    print("✅ Agent Core is available")
    print(get_agent_core_info())
else:
    print("❌ Agent Core not configured")
```

### 2. **Test Dual Mode**

```python
# Test with Agent Core
response1 = await agent.invoke_bedrock("Test query", use_agent_core=True)

# Test with direct Bedrock
response2 = await agent.invoke_bedrock("Test query", use_agent_core=False)

print(f"Agent Core: {response1}")
print(f"Direct Bedrock: {response2}")
```

## 🚀 Deployment

### 1. **Local Development**

```bash
# Set environment variables
export USE_BEDROCK_AGENT_CORE=true
export BEDROCK_AGENT_ID=ag-xxxxxxxx
export BEDROCK_AGENT_ALIAS_ID=ag-alias-xxxxxxxx

# Run the application
python -m streamlit run streamlit_app_simple.py
```

### 2. **EC2 Deployment**

```bash
# Update .env file on EC2
ssh -i key.pem ec2-user@your-ec2-ip 'cd /opt/career-guidance && echo "USE_BEDROCK_AGENT_CORE=true" >> .env'

# Restart services
ssh -i key.pem ec2-user@your-ec2-ip 'cd /opt/career-guidance && pkill -f uvicorn && nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &'
```

## 🔍 Monitoring

### 1. **Logs**

Check logs for Agent Core usage:

```bash
# Backend logs
tail -f logs/career_guidance_system.log | grep "Agent Core"

# Agent logs
tail -f logs/JobMarketAgent.log | grep "Agent Core"
```

### 2. **Health Check**

The health endpoint shows Agent Core status:

```bash
curl http://localhost:8000/health
```

Response includes:
```json
{
  "overall_status": "healthy",
  "agents": {
    "job_market": {
      "status": "healthy",
      "bedrock_client_available": true,
      "agent_core_available": true
    }
  }
}
```

## 🎯 Best Practices

### 1. **When to Use Agent Core**

- ✅ Complex multi-step queries
- ✅ Planning and orchestration needed
- ✅ Tool integration required
- ✅ Advanced context management

### 2. **When to Use Direct Bedrock**

- ✅ Simple, direct questions
- ✅ Performance-critical applications
- ✅ Cost-sensitive use cases
- ✅ Standard AI responses

### 3. **Hybrid Approach**

```python
# Use Agent Core for complex queries
if is_complex_query(query):
    response = await agent.invoke_bedrock(prompt, use_agent_core=True)
else:
    response = await agent.invoke_bedrock(prompt, use_agent_core=False)
```

## 🐛 Troubleshooting

### Common Issues

1. **Agent Core Not Available**
   ```
   Error: No Bedrock Agent Core configured
   ```
   **Solution**: Set `BEDROCK_AGENT_ID` and `BEDROCK_AGENT_ALIAS_ID`

2. **Permission Denied**
   ```
   Error: User is not authorized to perform: bedrock:InvokeAgent
   ```
   **Solution**: Add `bedrock:InvokeAgent` permission to IAM role

3. **Agent Not Found**
   ```
   Error: Agent ag-xxxxxxxx not found
   ```
   **Solution**: Verify Agent ID exists in the correct region

### Debug Mode

Enable detailed logging:

```bash
export LOG_LEVEL=DEBUG
export USE_BEDROCK_AGENT_CORE=true
```

## 📈 Performance Optimization

### 1. **Caching**

```python
# Cache Agent Core responses
@lru_cache(maxsize=100)
def cached_agent_core_response(query_hash):
    return invoke_agent_core(query)
```

### 2. **Async Processing**

```python
# Process multiple queries concurrently
tasks = [
    agent.invoke_bedrock(query1, use_agent_core=True),
    agent.invoke_bedrock(query2, use_agent_core=True)
]
results = await asyncio.gather(*tasks)
```

## 🎉 Summary

The Bedrock Agent Core integration provides:

- ✅ **Dual Mode Operation**: Choose between direct Bedrock and Agent Core
- ✅ **Enhanced Planning**: Intelligent task decomposition
- ✅ **Tool Orchestration**: Automatic tool selection and execution
- ✅ **Backward Compatibility**: Existing code works unchanged
- ✅ **Easy Configuration**: Simple environment variables
- ✅ **Comprehensive Logging**: Full visibility into operations

**Ready to use!** 🚀

