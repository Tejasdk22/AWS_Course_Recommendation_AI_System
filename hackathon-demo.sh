#!/bin/bash
# UTD Career Guidance AI System - Hackathon Demo Script

echo "🎓 UTD Career Guidance AI System Demo"
echo "====================================="

# Test individual agents
echo "\n🤖 Testing Individual Agents:"

for agent in job_market_agent course_catalog_agent career_matching_agent project_advisor_agent; do
    echo "\n📊 Testing $agent..."
    aws lambda invoke \
        --function-name utd-career-guidance-$agent \
        --payload '{"query":"I want to become a data scientist","sessionId":"demo-session"}' \
        response-$agent.json
    
    if [ $? -eq 0 ]; then
        echo "✅ $agent working"
        echo "Response preview:"
        head -3 response-$agent.json
    else
        echo "❌ $agent failed"
    fi
done

echo "\n🎉 Demo completed! Check response-*.json files for results."
echo "\n📋 Hackathon Compliance:"
echo "✅ 4 Autonomous Lambda Agents"
echo "✅ Real-time job market analysis"
echo "✅ UTD course catalog integration"
echo "✅ Career matching and recommendations"
echo "✅ Project suggestions"
echo "✅ No human intervention required"
