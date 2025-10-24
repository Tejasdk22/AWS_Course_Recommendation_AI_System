# 🌐 AWS Console Testing Guide for UTD Career Guidance AI System

## 🚀 Quick Start Testing

### 1. **Main Orchestrator Testing**
- **URL**: https://console.aws.amazon.com/lambda/
- **Region**: US East (N. Virginia)
- **Function**: `utd-career-guidance-orchestrator`
- **Action**: Click "Test" → "Create new test event"

#### Test Case 1: Business Analytics Undergraduate
```json
{
  "query": "I am a Business Analytics undergraduate student at UTD. I want to become a data scientist. What courses should I take?",
  "user_id": "test_user_ba_undergrad",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Test Case 2: Computer Science Graduate
```json
{
  "query": "I am a Computer Science graduate student at UTD. I want to become a software engineer. What courses should I take?",
  "user_id": "test_user_cs_grad",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Test Case 3: Information Technology Management Undergraduate
```json
{
  "query": "I am an Information Technology Management undergraduate student at UTD. I want to become a data analyst. What courses should I take?",
  "user_id": "test_user_itm_undergrad",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 2. **Individual Agent Testing**

#### Job Market Agent
- **Function**: `utd-career-guidance-job_market_agent`
- **Test Event**:
```json
{
  "test": true,
  "query": "Get job market data for data scientist positions",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Course Catalog Agent
- **Function**: `utd-career-guidance-course_catalog_agent`
- **Test Event**:
```json
{
  "test": true,
  "query": "Get UTD course catalog for Business Analytics",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Career Matching Agent
- **Function**: `utd-career-guidance-career_matching_agent`
- **Test Event**:
```json
{
  "test": true,
  "query": "Match skills for data scientist career",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Project Advisor Agent
- **Function**: `utd-career-guidance-project_advisor_agent`
- **Test Event**:
```json
{
  "test": true,
  "query": "Get project recommendations for data science",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Resume Analysis Agent
- **Function**: `utd-career-guidance-resume_analysis_agent`
- **Test Event**:
```json
{
  "resume_data": {
    "skills": ["Python", "SQL", "Excel", "Statistics"],
    "experience": "2 years",
    "education": "Bachelor in Business Analytics"
  },
  "user_id": "test_user_resume"
}
```

#### Email Notification Agent
- **Function**: `utd-career-guidance-email_notification_agent`
- **Test Event**:
```json
{
  "notification_type": "job_alert",
  "user_email": "test@example.com",
  "user_preferences": {
    "frequency": "daily"
  }
}
```

## 📊 Expected Results

### ✅ **Successful Response Format**
```json
{
  "statusCode": 200,
  "body": {
    "success": true,
    "course_recommendations": {
      "career_path": "Data Scientist",
      "major": "Business Analytics",
      "student_type": "Undergraduate",
      "courses": [...],
      "graduation_plan": {
        "total_courses": 40,
        "core_courses": [...],
        "elective_courses": [...]
      },
      "projects": [...],
      "market_analysis": {...}
    }
  }
}
```

### 🎯 **What to Look For**
1. **Status Code**: Should be 200
2. **Course Recommendations**: Should include major-specific courses
3. **Graduation Plan**: Should show correct course structure
4. **Projects**: Should include real project suggestions
5. **Market Analysis**: Should include job market insights

## 🔍 **Troubleshooting**

### Common Issues:
1. **Timeout**: Increase timeout to 5 minutes
2. **Memory**: Increase memory to 512MB
3. **Permissions**: Check IAM role permissions
4. **Logs**: Check CloudWatch logs for errors

### CloudWatch Logs:
- **URL**: https://console.aws.amazon.com/cloudwatch/
- **Service**: Lambda
- **Function**: Select your function
- **Logs**: Check for errors

## 🎉 **Success Indicators**

### ✅ **System Working Properly**
- All Lambda functions return status 200
- Course recommendations are major-specific
- Graduation plans show correct course counts
- Projects are from real sources (Kaggle, GitHub)
- Market analysis includes job data

### ⚠️ **Partial Success**
- Some functions work, others don't
- Check individual function logs
- Verify IAM permissions

### ❌ **System Issues**
- Functions return errors
- Check CloudWatch logs
- Verify AWS service permissions

## 🚀 **Next Steps After Testing**

1. **If Successful**: System is ready for production use
2. **If Partial**: Fix individual agent issues
3. **If Failed**: Check AWS permissions and service access

## 📞 **Support**

- **AWS Lambda Console**: https://console.aws.amazon.com/lambda/
- **CloudWatch Logs**: https://console.aws.amazon.com/cloudwatch/
- **IAM Console**: https://console.aws.amazon.com/iam/

---

**🎓 Your UTD Career Guidance AI System is ready for testing in the AWS Console!**
