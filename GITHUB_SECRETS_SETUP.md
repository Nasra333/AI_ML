# GitHub Secrets Setup for Railway Deployment

## ⚠️ Action Required: Configure GitHub Secrets

Your GitHub Actions workflow is failing because the required Railway secrets are not configured.

---

## 🔑 Required Secrets

You need to add these secrets to your GitHub repository:

### 1. RAILWAY_TOKEN (Required)
- **Purpose**: Authenticates GitHub Actions with Railway API
- **How to get it**:
  1. Go to [Railway Dashboard](https://railway.app/account/tokens)
  2. Click **"Create Token"** or **"New Token"**
  3. Give it a name (e.g., "GitHub Actions Deploy")
  4. Copy the generated token (you'll only see it once!)

### 2. RAILWAY_SERVICE_ID (Optional but Recommended)
- **Purpose**: Specifies which Railway service to deploy to
- **How to get it**:
  1. Go to your Railway project dashboard
  2. Click on your service
  3. Go to **Settings** tab
  4. Copy the **Service ID** (found under "Service ID" section)

---

## 📝 How to Add Secrets to GitHub

### Step-by-Step Instructions:

1. **Navigate to Your Repository**
   - Go to `https://github.com/YOUR_USERNAME/AI_ML`

2. **Open Settings**
   - Click on **Settings** tab (top right)

3. **Access Secrets**
   - In the left sidebar, click **Secrets and variables** → **Actions**

4. **Add New Secret**
   - Click **"New repository secret"** button

5. **Add RAILWAY_TOKEN**
   - Name: `RAILWAY_TOKEN`
   - Value: Paste your Railway token
   - Click **"Add secret"**

6. **Add RAILWAY_SERVICE_ID** (Optional)
   - Click **"New repository secret"** again
   - Name: `RAILWAY_SERVICE_ID`
   - Value: Paste your Railway service ID
   - Click **"Add secret"**

---

## 🔍 Verify Secrets Are Added

After adding secrets, you should see them listed under:
- **Settings** → **Secrets and variables** → **Actions** → **Repository secrets**

You should see:
- ✅ `RAILWAY_TOKEN`
- ✅ `RAILWAY_SERVICE_ID` (if added)

---

## 🚀 Re-run the Workflow

Once secrets are added:

1. Go to **Actions** tab in your GitHub repository
2. Find the failed workflow run
3. Click **"Re-run all jobs"**

Or simply push a new commit:
```bash
git commit --allow-empty -m "Trigger deployment after adding secrets"
git push origin main
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep your Railway token secret
- Rotate tokens periodically
- Use different tokens for different environments
- Delete tokens you're no longer using

### ❌ DON'T:
- Never commit tokens to your repository
- Don't share tokens in chat or email
- Don't use the same token across multiple projects
- Don't store tokens in plain text files

---

## 🐛 Troubleshooting

### Error: "Project Token not found"
**Solution**: Add `RAILWAY_TOKEN` secret to GitHub repository

### Error: "Service not found"
**Solution**: 
- Add `RAILWAY_SERVICE_ID` secret, OR
- Remove the `service:` line from workflow file to deploy to default service

### Error: "Invalid token"
**Solution**: 
- Generate a new token from Railway dashboard
- Update the `RAILWAY_TOKEN` secret in GitHub

### Deployment succeeds but app doesn't work
**Solution**: 
- Check Railway dashboard logs
- Verify environment variables are set in Railway:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `GOOGLE_API_KEY`
  - `PORT` (set to 7860)
  - `GRADIO_SERVER_NAME` (set to 0.0.0.0)

---

## 📋 Quick Checklist

Before re-running the workflow, ensure:

- [ ] Railway account is created
- [ ] Railway project exists
- [ ] Railway token is generated
- [ ] `RAILWAY_TOKEN` secret is added to GitHub
- [ ] `RAILWAY_SERVICE_ID` secret is added (optional)
- [ ] Environment variables are set in Railway dashboard
- [ ] Latest code is pushed to GitHub

---

## 🔗 Useful Links

- **Railway Tokens**: https://railway.app/account/tokens
- **Railway Dashboard**: https://railway.app/dashboard
- **GitHub Secrets Docs**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Railway Deployment Docs**: https://docs.railway.app/deploy/deployments

---

## 💡 Alternative: Deploy Without GitHub Actions

If you prefer to deploy directly without GitHub Actions:

1. **Using Railway CLI**:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Link to project
   railway link
   
   # Deploy
   railway up
   ```

2. **Using Railway Dashboard**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-deploy on every push

---

## ✨ What Happens After Setup

Once secrets are configured and workflow runs successfully:

1. ✅ Every push to `main` branch triggers automatic deployment
2. ✅ GitHub Actions builds and tests your code
3. ✅ Railway receives deployment trigger
4. ✅ Railway builds and deploys your app
5. ✅ Your app is live at your Railway URL

---

*Last Updated: October 2025*
*For more help, see: RAILWAY_DEPLOYMENT.md*
