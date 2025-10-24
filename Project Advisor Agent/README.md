# 🧠 Project Advisor Agent (AWS Lambda)

This AWS Lambda function acts as a **Project Advisor Agent**, dynamically recommending projects and certifications for both technical and non-technical roles.  
It scrapes data from **GitHub**, **Forage**, **Oracle**, **Snowflake**, and other public certification websites, then uses **AWS Bedrock (Claude 3.5 Haiku)** for reasoning and summarization.

---

## ⚙️ Setup Guide

### 1️⃣ Create Lambda Function
1. Go to **AWS Console → Lambda → Create Function**
2. Choose:
   - **Author from scratch**
   - Function name: `ProjectAdvisorAgent`
   - Runtime: **Python 3.12**
   - Architecture: `x86_64`
   - Handler: `lambda_function.lambda_handler`
3. Click **Create Function**

---

### 2️⃣ Upload the Code
1. Zip the following files:
   - `lambda_function.py`
   - `requirements.txt`
   - `README.md`
2. In your Lambda function console:
   - Go to **Code → Upload from → .zip file**
   - Upload your zip
   - Click **Deploy**

---

### 3️⃣ IAM Role Permissions
Attach these managed policies to your Lambda execution role:
- `AWSLambdaBasicExecutionRole`
- `AmazonBedrockFullAccess`

If your Lambda uses outbound internet requests (for web scraping with `requests`):
- Ensure your Lambda **is not inside a private VPC**, or
- Configure **VPC + NAT Gateway** to allow internet access.

---

### 4️⃣ Environment Variables (Optional)
To easily swap Bedrock models later:
1. Go to **Configuration → Environment Variables**
2. Add:
   ```
   BEDROCK_MODEL_ID = arn:aws:bedrock:us-east-2:831981619381:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0
   ```

---

### 5️⃣ Test the Lambda
Click **Test** in the AWS Lambda console and use this sample input:
```json
{
  "body": "{"role": "Data Analyst", "student_level": "Undergraduate"}"
}
```

You’ll get an AI-generated response with:
- 3 project recommendations
- 3 certification suggestions
- Links to live sources (GitHub, Forage, Oracle, Snowflake, etc.)

---

### 6️⃣ Integrate with Bedrock Master Agent (Optional)
To let your **Bedrock Master Agent** trigger this Lambda:

1. Go to **Amazon Bedrock → Agents → [Your Master Agent]**
2. Add a new **Action Group**
3. Select this Lambda (`ProjectAdvisorAgent`)
4. Add this permission to your Lambda resource policy:
   ```json
   {
     "Effect": "Allow",
     "Principal": {"Service": "bedrock.amazonaws.com"},
     "Action": "lambda:InvokeFunction",
     "Resource": "arn:aws:lambda:us-east-2:<your-account-id>:function:ProjectAdvisorAgent"
   }
   ```
5. Deploy your Bedrock agent.

---

### 7️⃣ Example Output
```json
{
  "role": "Data Scientist",
  "level": "Undergraduate",
  "ai_summary": {
    "projects": [
      {"title": "Customer Churn Predictor", "skills": ["Python", "Machine Learning", "Visualization"]},
      {"title": "COVID-19 Dashboard", "skills": ["Plotly", "Streamlit", "SQL"]}
    ],
    "certifications": [
      {"title": "IBM Data Science Professional Certificate", "platform": "Coursera"},
      {"title": "Azure Data Scientist Associate", "platform": "Microsoft Learn"}
    ]
  }
}
```

---

### 8️⃣ Share This Project
To share your Lambda project:
1. Zip this folder:  
   `lambda_function.py`, `requirements.txt`, `README.md`
2. Share via:
   - **GitHub**
   - **Google Drive**
   - **Email or cloud link**

Provide:
- Region: `us-east-2`
- Runtime: `Python 3.12`
- Handler: `lambda_function.lambda_handler`
- Permissions: Bedrock + Basic Execution

---

### 🧩 Notes
- This agent is **stateless** (no vector database or persistent storage).  
- It fetches **live data on demand** using public APIs and search endpoints.  
- Can be extended later with OpenSearch or DynamoDB for history tracking.
