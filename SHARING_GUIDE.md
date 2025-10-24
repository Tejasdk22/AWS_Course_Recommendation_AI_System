# 🌐 How to Share Your UTD Course Recommendation AI

## 🚀 Quick Sharing Options

### Option 1: Same WiFi Network (Immediate)
If they're on the same WiFi network as you:
- **URL**: http://192.168.1.182:8503
- **Status**: ✅ **Working right now**
- **Limitation**: Only works on same local network

### Option 2: Deploy to Streamlit Cloud (Free & Easy)
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "UTD Course Recommendation AI"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Connect your GitHub repository
   - Set main file to: `streamlit_app_simple.py`
   - Deploy!

3. **Get your public URL**: `https://your-username-streamlit-app.streamlit.app`

### Option 3: Use ngrok (Quick but requires account)
1. **Sign up**: https://dashboard.ngrok.com/signup
2. **Get authtoken**: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Install token**: `ngrok authtoken YOUR_TOKEN`
4. **Expose app**: `ngrok http 8503`
5. **Share URL**: Use the public URL provided

### Option 4: Use localtunnel (No account needed)
1. **Install**: `npm install -g localtunnel`
2. **Expose app**: `lt --port 8503`
3. **Share URL**: Use the public URL provided

### Option 5: Deploy to Heroku (Free tier)
1. **Create Procfile**:
   ```
   web: streamlit run streamlit_app_simple.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

3. **Get URL**: `https://your-app-name.herokuapp.com`

## 🎯 Recommended Approach

**For immediate sharing**: Use **Option 1** (same WiFi)
**For permanent sharing**: Use **Option 2** (Streamlit Cloud)

## 📱 Current Status
- ✅ **Streamlit App**: http://localhost:8503
- ✅ **Network Access**: http://192.168.1.182:8503
- ✅ **UTD-Specific**: All course codes and recommendations are UTD-specific

## 🎓 UTD Features
- Real UTD course codes (BUAN, MIS, CS, ITSS, MATH, STAT)
- UTD-specific resources and opportunities
- UTD academic timeline and planning
- UTD campus organizations and faculty connections
