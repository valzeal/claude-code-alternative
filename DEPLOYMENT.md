# Zeal Code - Deployment Guide

Deploy Zeal Code to production for free using Render.com.

## Prerequisites

1. **GitHub Account**: Your code must be on GitHub
2. **Render Account**: Sign up at https://render.com (free tier available)
3. **Repository**: Ensure `claude-code-alternative` is pushed to GitHub

## Deployment Options

### Option 1: Deploy via Render Dashboard (Recommended for First Time)

#### Deploy the API Service

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select the `claude-code-alternative` repository
5. Configure the service:
   - **Name**: `zeal-code-api`
   - **Environment**: `Python 3`
   - **Branch**: `main`
   - **Root Directory**: `./` (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api_framework.main:app --host 0.0.0.0 --port $PORT`
6. Click **"Deploy Web Service"**

#### Deploy the UI Service

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Select the same repository (`claude-code-alternative`)
4. Configure the service:
   - **Name**: `zeal-code-ui`
   - **Environment**: `Python 3`
   - **Branch**: `main`
   - **Root Directory**: `./` (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run ui/web_interface.py --server.port $PORT --server.address 0.0.0.0`
5. Click **"Deploy Web Service"**

### Option 2: Deploy via render.yaml (Automated)

1. Make sure `render.yaml` is in your repository root
2. Go to https://dashboard.render.com/
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub account
5. Select the `claude-code-alternative` repository
6. Render will automatically detect and deploy both services
7. Click **"Apply Blueprint"**

## Accessing Your Deployment

After deployment completes (usually 2-5 minutes):

- **API URL**: `https://zeal-code-api.onrender.com`
- **UI URL**: `https://zeal-code-ui.onrender.com`

## Testing Your Deployment

### Test the API

```bash
curl https://zeal-code-api.onrender.com/
```

Expected response:
```json
{
  "status": "running",
  "service": "Zeal Code API"
}
```

### Test the UI

Open `https://zeal-code-ui.onrender.com` in your browser.

## Free Tier Limits

Render Free Tier includes:
- ✅ 750 hours/month of web service time
- ✅ Automatic SSL certificates
- ✅ 512MB RAM
- ✅ 0.1 CPU
- ✅ 100GB outbound bandwidth

This is sufficient for:
- Development and testing
- Small projects
- Personal use

## Custom Domain Setup (Optional)

If you have a custom domain:

1. Go to your service in Render Dashboard
2. Click **"Custom Domains"**
3. Click **"Add Domain"**
4. Follow the DNS setup instructions

## Environment Variables

To add environment variables:

1. Go to your service in Render Dashboard
2. Click **"Environment"**
3. Add variables as needed

Example variables:
- `API_KEY`: Your API key
- `ENABLE_CACHING`: `true`
- `MAX_CACHE_SIZE`: `1000`

## Monitoring and Logs

View logs:
1. Go to your service in Render Dashboard
2. Click **"Logs"**

Monitor performance:
1. Go to your service in Render Dashboard
2. Click **"Metrics"**

## Scaling

To upgrade from free tier:

1. Go to your service in Render Dashboard
2. Click **"Settings"**
3. Change the plan under **"Plan"**

## Troubleshooting

### Build Failures

Check the build logs for errors:
1. Go to your service
2. Click **"Logs"**
3. Look for "Build" section

Common issues:
- Missing dependencies → Update `requirements.txt`
- Python version mismatch → Ensure Python 3.11+
- Import errors → Check module paths

### Service Crashes

Check runtime logs:
1. Go to your service
2. Click **"Logs"**
3. Look for error messages

Common issues:
- Port binding errors → Ensure using `$PORT`
- Memory limits → Upgrade plan
- Timeout errors → Increase `UVICORN_TIMEOUT`

### 502 Bad Gateway

This usually means the service is starting up. Wait 1-2 minutes and try again.

## Alternative Free Deployment Platforms

### 1. Railway (railway.app)
- Free tier: $5/month credit
- Auto-deploys from GitHub
- Simple setup

### 2. Fly.io (fly.io)
- Free tier: 3 VMs × 256MB RAM
- Requires Dockerfile
- Global deployment

### 3. PythonAnywhere
- Free tier for web apps
- Limited always-on time
- Good for hobby projects

### 4. Replit
- Always-on Repls (paid now)
- Easy to use
- Good for development

### 5. Glitch
- Free for simple apps
- Limited resources
- Good for prototypes

## Production Checklist

Before going to production:

- [ ] Update API keys and secrets
- [ ] Configure environment variables
- [ ] Set up custom domain (optional)
- [ ] Enable SSL certificates (automatic on Render)
- [ ] Set up monitoring and alerts
- [ ] Configure backup strategy
- [ ] Test all endpoints
- [ ] Review logs for errors
- [ ] Update documentation
- [ ] Set up CI/CD pipeline (optional)

## Support

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: https://github.com/ridzeal/claude-code-alternative/issues

## Cost Summary

**Free Tier (Render)**:
- Cost: $0/month
- Limits: 750 hours/month, 512MB RAM
- Perfect for: Development, testing, personal projects

**Paid Tier** (if needed):
- Standard: $7/month (512MB RAM, 0.5 CPU)
- Starter: $25/month (2GB RAM, 1 CPU)

---

**Ready to deploy?** Start with Option 1 (Dashboard) for the easiest experience!
