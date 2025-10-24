# 🚀 Streamlit Cloud Deployment Guide

## 📋 Prerequisites

### **Required Accounts**
- ✅ **GitHub Account**: For code repository
- ✅ **Streamlit Cloud Account**: Free at https://share.streamlit.io/
- ✅ **AWS Account**: For Bedrock AI (optional for demo)

### **Required Files**
- ✅ `streamlit_app_simple.py` - Main Streamlit application
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Project documentation

## 🎯 Step-by-Step Deployment

### **Step 1: Prepare Your Repository**

#### **1.1 Create GitHub Repository**
```bash
# Create a new repository on GitHub
# Name: utd-course-recommendation-ai
# Description: UTD Course Recommendation AI System
# Visibility: Public (required for free Streamlit Cloud)
```

#### **1.2 Push Your Code**
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "UTD Course Recommendation AI - Streamlit Cloud Ready"

# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/utd-course-recommendation-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### **Step 2: Deploy to Streamlit Cloud**

#### **2.1 Access Streamlit Cloud**
1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Authorize** Streamlit to access your repositories

#### **2.2 Create New App**
1. **Click**: "New app" button
2. **Repository**: Select `YOUR_USERNAME/utd-course-recommendation-ai`
3. **Branch**: `main`
4. **Main file path**: `streamlit_app_simple.py`
5. **App URL**: Choose a custom URL (optional)
   - Example: `utd-course-recommendation-ai`
6. **Click**: "Deploy!"

#### **2.3 Wait for Deployment**
- **Status**: "Deploying..." → "Running"
- **Time**: 2-5 minutes
- **URL**: `https://your-username-streamlit-app.streamlit.app`

## 🎉 Your App is Live!

### **Access Your App**
- **URL**: `https://your-username-streamlit-app.streamlit.app`
- **Status**: ✅ **Public and accessible worldwide**
- **Features**: All UTD-specific features working

### **Share Your App**
- **Direct Link**: Share the Streamlit Cloud URL
- **Social Media**: Post on LinkedIn, Twitter, etc.
- **Email**: Send to colleagues and students
- **Presentations**: Use in demos and presentations

## 🔧 Configuration Options

### **Environment Variables (Optional)**
If you want to use the full AI backend:

1. **Go to**: Streamlit Cloud dashboard
2. **Select your app**
3. **Click**: "Settings"
4. **Add secrets**:
   ```toml
   [secrets]
   AWS_ACCESS_KEY_ID = "your_access_key"
   AWS_SECRET_ACCESS_KEY = "your_secret_key"
   AWS_DEFAULT_REGION = "us-east-1"
   ```

### **App Settings**
- **Python Version**: 3.8+ (automatic)
- **Memory**: 1GB (free tier)
- **CPU**: 1 core (free tier)
- **Storage**: 1GB (free tier)

## 📱 App Features

### **What Users Can Do**
1. **Select Major**: Business Analytics, Data Science, Computer Science, etc.
2. **Choose Student Type**: Undergraduate or Graduate
3. **Set Career Goal**: Data Scientist, Data Engineer, etc.
4. **Get Recommendations**: Personalized course suggestions
5. **Explore Results**: Detailed career guidance

### **UTD-Specific Features**
- ✅ **Real UTD Course Codes**: BUAN, MIS, CS, ITSS, MATH, STAT
- ✅ **Campus Resources**: Student organizations, faculty connections
- ✅ **Academic Timeline**: Semester-by-semester planning
- ✅ **Career Services**: UTD-specific opportunities

## 🚀 Advanced Deployment

### **Custom Domain (Paid)**
1. **Upgrade to Pro**: $20/month
2. **Add custom domain**: `your-domain.com`
3. **SSL Certificate**: Automatic HTTPS

### **Private Repository (Paid)**
1. **Upgrade to Pro**: $20/month
2. **Private repos**: Access to private GitHub repositories
3. **Team collaboration**: Multiple developers

### **Scaling Options**
- **Pro Plan**: $20/month for production use
- **Enterprise**: Custom pricing for large organizations
- **Self-hosted**: Deploy on your own infrastructure

## 🔄 Updates and Maintenance

### **Automatic Updates**
- **GitHub Integration**: Updates when you push to main branch
- **Automatic Deployment**: Streamlit Cloud rebuilds automatically
- **Zero Downtime**: Updates happen seamlessly

### **Manual Updates**
1. **Make changes** to your code
2. **Commit and push** to GitHub
3. **Streamlit Cloud** automatically detects changes
4. **App updates** in 2-3 minutes

### **Monitoring**
- **Usage Analytics**: Track app usage
- **Error Logs**: Monitor for issues
- **Performance Metrics**: CPU and memory usage

## 🛠️ Troubleshooting

### **Common Issues**

#### **App Won't Deploy**
- **Check**: Main file path is correct (`streamlit_app_simple.py`)
- **Check**: Requirements.txt exists
- **Check**: Repository is public (free tier)

#### **App Crashes**
- **Check**: All dependencies in requirements.txt
- **Check**: No syntax errors in code
- **Check**: AWS credentials (if using AI features)

#### **Slow Performance**
- **Check**: App is using cached data
- **Check**: No infinite loops in code
- **Check**: Memory usage within limits

### **Debug Steps**
1. **Check logs**: Streamlit Cloud dashboard
2. **Test locally**: Run `streamlit run streamlit_app_simple.py`
3. **Verify dependencies**: Check requirements.txt
4. **Contact support**: Streamlit Cloud support

## 📊 Analytics and Monitoring

### **Usage Analytics**
- **Page Views**: Track app usage
- **User Sessions**: Monitor engagement
- **Geographic Data**: See where users are from
- **Performance Metrics**: Load times and errors

### **Error Monitoring**
- **Error Logs**: Automatic error tracking
- **Performance Alerts**: Notifications for issues
- **Uptime Monitoring**: Track app availability

## 🎯 Best Practices

### **Code Organization**
- **Keep main file simple**: Use `streamlit_app_simple.py`
- **Separate logic**: Move complex code to modules
- **Error handling**: Add try-catch blocks
- **Documentation**: Update README regularly

### **Performance Optimization**
- **Caching**: Use `@st.cache_data` for expensive operations
- **Lazy loading**: Load data only when needed
- **Efficient queries**: Optimize database calls
- **Memory management**: Clean up large objects

### **Security**
- **Secrets management**: Use Streamlit secrets for sensitive data
- **Input validation**: Validate user inputs
- **Rate limiting**: Prevent abuse
- **HTTPS**: Always use secure connections

## 🎓 UTD-Specific Deployment

### **Campus Integration**
- **Share with UTD**: Send to career services
- **Student Organizations**: Share with Data Science Society
- **Faculty**: Show to professors
- **Academic Advisors**: Use for student guidance

### **Marketing Your App**
- **LinkedIn**: Post about your project
- **GitHub**: Star and share repository
- **Portfolio**: Add to your resume
- **Presentations**: Use in job interviews

## 📞 Support and Resources

### **Streamlit Cloud Support**
- **Documentation**: https://docs.streamlit.io/
- **Community**: https://discuss.streamlit.io/
- **GitHub Issues**: Report bugs and feature requests

### **UTD Resources**
- **Career Services**: UTD career guidance
- **Academic Advisors**: Course planning help
- **Student Organizations**: Data Science Society, Analytics Club
- **Faculty**: Professor research areas

---

## 🎉 Congratulations!

Your UTD Course Recommendation AI is now live on Streamlit Cloud! 

**Share your app**: `https://your-username-streamlit-app.streamlit.app`

This system provides personalized career guidance specifically for UTD students, combining real course data with AI-powered insights to help students make informed decisions about their academic and career paths.
