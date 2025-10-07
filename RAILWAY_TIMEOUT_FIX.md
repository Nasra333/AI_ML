# Railway Build Timeout Fix

## Problem
Railway builds were timing out due to:
1. **Massive dependencies** - 51 packages including PyTorch (700MB+), transformers (1GB+), langchain ecosystem
2. **Nixpacks overhead** - Nix environment setup adds 1m+ to build time
3. **No build optimization** - Installing packages not actually used in production

## Root Cause
Your `requirements.txt` included development dependencies (JupyterLab, wandb) and heavy ML libraries (torch, transformers) that aren't actually imported in the production code.

## Solution Implemented

### 1. Created `requirements-prod.txt` (Minimal Production Dependencies)
- **Reduced from 51 to 11 packages**
- Only includes packages actually imported:
  - gradio (web framework)
  - openai, anthropic, google-generativeai (AI APIs)
  - PyPDF2, python-docx (document processing)
  - beautifulsoup4, requests (web scraping)

### 2. Created `Dockerfile` for Better Build Control
- Uses `python:3.11-slim` base image
- Layer caching for faster rebuilds
- `--no-cache-dir` flag to reduce image size

### 3. Updated `railway.json`
- Changed builder from `NIXPACKS` to `DOCKERFILE`
- This gives you full control over the build process

### 4. Created `nixpacks.toml` (Alternative)
- If you prefer Nixpacks, this config uses `requirements-prod.txt`
- To use: change `railway.json` back to `"builder": "NIXPACKS"`

### 5. Enhanced `.dockerignore`
- Excludes all documentation and dev files
- Prevents copying unnecessary files to build context

## Deployment Options

### Option A: Use Dockerfile (Current Configuration - RECOMMENDED)
```bash
# Already configured in railway.json
# Just commit and push
git add .
git commit -m "Fix Railway timeout with optimized Dockerfile"
git push
```

**Expected build time: 2-4 minutes** (down from 10+ minutes)

### Option B: Use Nixpacks with Optimization
1. Update `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```
2. Commit and push

**Expected build time: 3-5 minutes**

## Verification Steps

After deployment:
1. Check Railway logs for build time
2. Verify all tabs work (Job Match, Study Notes, Generic)
3. Test document upload functionality
4. Test AI responses with all three providers

## If You Need Heavy ML Libraries

If you actually need torch/transformers/langchain in production:
1. Add them back to `requirements-prod.txt`
2. Consider Railway Pro plan (longer build timeout)
3. Use pre-built Docker images with ML libraries
4. Or use Railway's persistent volumes for model caching

## Keep Development Dependencies Separate

- `requirements.txt` - Full dev environment (local use)
- `requirements-prod.txt` - Production only (Railway)

This separation keeps builds fast and deployments lean.
