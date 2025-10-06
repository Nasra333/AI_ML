# Railway Deployment Guide

This guide provides detailed instructions for deploying the AI_ML Gradio application to Railway.

## Overview

Railway is a modern platform-as-a-service (PaaS) that simplifies application deployment. This project is configured to deploy seamlessly on Railway with minimal setup.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app/)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **API Keys**: Obtain API keys from:
   - [OpenAI](https://platform.openai.com/api-keys)
   - [Anthropic](https://console.anthropic.com/)
   - [Google AI](https://makersuite.google.com/app/apikey)

## Deployment Steps

### Step 1: Create a New Railway Project

1. Log in to [Railway](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account (if first time)
5. Select the repository containing this project

### Step 2: Configure Environment Variables

Railway needs your API keys to function properly. Add these in the Railway dashboard:

1. In your Railway project, click on your service
2. Go to the **"Variables"** tab
3. Add the following environment variables:

```bash
OPENAI_API_KEY=<your-openai-api-key>
ANTHROPIC_API_KEY=<your-anthropic-api-key>
GOOGLE_API_KEY=<your-google-api-key>
PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
```

**Important Notes:**
- Replace the placeholder values with your actual API keys
- `PORT` and `GRADIO_SERVER_NAME` are pre-configured but can be customized
- Never commit API keys to your repository

### Step 3: Deploy

Railway will automatically:
1. Detect the `Procfile` and start command
2. Install Python dependencies from `requirements.txt`
3. Build and deploy your application
4. Assign a public URL

**Build Process:**
- Railway uses Nixpacks to detect and build Python applications
- Dependencies are installed via pip
- The application starts using the command in `Procfile`

### Step 4: Access Your Application

1. Once deployment completes, Railway provides a public URL
2. Click **"Settings"** → **"Networking"** → **"Generate Domain"**
3. Your app will be accessible at: `https://your-app-name.up.railway.app`

## Configuration Files

### `Procfile`
Defines the command to start the application:
```
web: python app.py
```

### `railway.json`
Railway-specific configuration:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `runtime.txt`
Specifies Python version:
```
python-3.11.0
```

### `.env.example`
Template for environment variables (not deployed, for reference only)

## Monitoring and Logs

### View Logs
1. Go to your Railway project dashboard
2. Click on your service
3. Select the **"Deployments"** tab
4. Click on the latest deployment to view logs

### Common Log Messages
- `Running on http://0.0.0.0:7860` - Application started successfully
- `Keyboard interrupt received` - Application stopped
- `ModuleNotFoundError` - Missing dependency (check requirements.txt)

## Troubleshooting

### Build Failures

**Problem**: Dependencies fail to install
**Solution**: 
- Check `requirements.txt` for syntax errors
- Verify package names are correct
- Some packages may require system dependencies

**Problem**: Python version mismatch
**Solution**: 
- Update `runtime.txt` to match your development environment
- Supported versions: 3.8, 3.9, 3.10, 3.11, 3.12

### Runtime Errors

**Problem**: Application crashes on startup
**Solution**:
- Check Railway logs for error messages
- Verify all environment variables are set
- Ensure API keys are valid

**Problem**: API calls fail
**Solution**:
- Verify API keys in Railway environment variables
- Check API key permissions and quotas
- Ensure no extra spaces in environment variable values

**Problem**: Port binding errors
**Solution**:
- Railway automatically sets the `PORT` variable
- Ensure your app reads from `os.getenv("PORT", "7860")`

### Performance Issues

**Problem**: Slow response times
**Solution**:
- Railway free tier has limited resources
- Consider upgrading to a paid plan for better performance
- Optimize model calls and caching

**Problem**: Application timeout
**Solution**:
- Gradio applications may take time to load large models
- Increase timeout settings in Railway if needed
- Consider lazy loading for heavy dependencies

## Cost Considerations

### Railway Pricing
- **Free Tier**: $5 of usage credits per month
- **Pro Plan**: $20/month with additional usage credits
- **Usage-based**: Charged per resource consumption

### Optimization Tips
1. **Use CPU-optimized models**: The project uses PyTorch CPU version
2. **Monitor usage**: Check Railway dashboard for resource consumption
3. **Implement caching**: Cache model responses when appropriate
4. **Rate limiting**: Consider implementing rate limits for API calls

## Security Best Practices

1. **Never commit `.env` files**: Already in `.gitignore`
2. **Rotate API keys regularly**: Update in Railway dashboard
3. **Use Railway secrets**: For sensitive configuration
4. **Enable HTTPS**: Railway provides SSL certificates automatically
5. **Monitor access logs**: Check for unusual activity

## Updating Your Deployment

### Push Updates
1. Commit changes to your GitHub repository
2. Push to the main branch
3. Railway automatically detects changes and redeploys

### Manual Redeploy
1. Go to Railway dashboard
2. Click on your service
3. Click **"Redeploy"** button

### Rollback
1. Go to **"Deployments"** tab
2. Find a previous successful deployment
3. Click **"Redeploy"** on that version

## Custom Domain (Optional)

1. Go to **"Settings"** → **"Networking"**
2. Click **"Custom Domain"**
3. Add your domain name
4. Configure DNS records as instructed by Railway

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Gradio Documentation](https://www.gradio.app/docs/)
- [Railway Discord Community](https://discord.gg/railway)

## Support

If you encounter issues:
1. Check Railway logs for error messages
2. Review this troubleshooting guide
3. Consult Railway documentation
4. Ask in Railway Discord community
5. Open an issue in the project repository

---

**Last Updated**: October 2025
**Railway Version**: Latest
**Gradio Version**: Check requirements.txt
