# 🚀 Quick Deploy to Railway - 5 Minutes

## Prerequisites
- ✅ Railway account ([Sign up here](https://railway.app/))
- ✅ API Keys ready (OpenAI, Anthropic, Google AI)

---

## Step 1: Push to GitHub (if not already done)
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

---

## Step 2: Create Railway Project
1. Go to **[railway.app](https://railway.app/)**
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **your repository**

---

## Step 3: Add Environment Variables
In Railway dashboard → **Variables** tab, add:

```bash
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
```

**⚠️ Important:** Replace with your actual API keys!

---

## Step 4: Generate Domain
1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Your app will be live at: `https://your-app.up.railway.app`

---

## Step 5: Test Your App
Visit your Railway URL and verify:
- ✅ Gradio interface loads
- ✅ Model selector works
- ✅ All tabs are accessible
- ✅ AI responses work

---

## 🎉 Done!
Your AI_ML Gradio app is now live on Railway!

---

## 📊 What Railway Will Do
1. **Detect** Python project
2. **Install** dependencies from `requirements.txt`
3. **Run** `python app.py` (from Procfile)
4. **Deploy** to public URL
5. **Monitor** and auto-restart on failures

---

## 🐛 If Something Goes Wrong

### Build Fails
- Check **Deployments** → **Build Logs**
- Verify `requirements.txt` has no errors

### App Crashes
- Check **Deployments** → **Deploy Logs**
- Verify all environment variables are set correctly

### Can't Access App
- Ensure domain is generated
- Check if deployment is "Active"

---

## 💰 Cost
- **Free Tier**: $5/month credits (good for testing)
- **Pro Plan**: $20/month + usage (recommended for production)

---

## 📚 Need More Help?
- **Detailed Guide**: See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)
- **Checklist**: See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- **Summary**: See [RAILWAY_SETUP_SUMMARY.md](./RAILWAY_SETUP_SUMMARY.md)

---

**Total Time**: ~5 minutes (excluding build time)
**Difficulty**: Easy ⭐
