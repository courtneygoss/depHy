# Render CLI Deployment Guide

## ✅ Your Changes Are Pushed to GitHub!

Your latest changes have been successfully pushed to GitHub. Now let's deploy using Render CLI.

## Step 1: Install Render CLI (Already Done!)

The Render CLI is already installed on your system:
```bash
render --version
# Output: render version 2.1.4
```

## Step 2: Authenticate with Render

```bash
render login
```

This will open your browser to authenticate with your Render account.

## Step 3: Deploy Your Application

### Option A: Deploy from render.yaml (Recommended)
```bash
# Deploy using your existing render.yaml configuration
render services create --from-manifest render.yaml
```

### Option B: Deploy interactively
```bash
# Start interactive deployment
render services create

# Follow the prompts:
# - Service Type: Web Service
# - Name: depHy
# - Environment: Python
# - Repository: Select your GitHub repo
# - Branch: main
# - Build Command: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
# - Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

## Step 4: Monitor Your Deployment

```bash
# View deployment logs
render logs --service depHy

# Check service status
render services list

# View specific service details
render services show depHy
```

## Step 5: Manage Your Deployment

```bash
# Trigger a new deployment
render deploys create --service depHy

# Restart the service
render restart depHy

# View recent deploys
render deploys list --service depHy
```

## Useful Render CLI Commands

### Authentication
```bash
render login          # Login to Render
render whoami         # Check current user
render logout         # Logout from Render
```

### Service Management
```bash
render services list                    # List all services
render services show <service-name>     # Show service details
render services delete <service-name>   # Delete a service
```

### Deployment Management
```bash
render deploys list --service <service-name>    # List deployments
render deploys show <deploy-id>                 # Show deployment details
render deploys create --service <service-name>  # Trigger new deployment
```

### Logs and Monitoring
```bash
render logs --service <service-name>    # View service logs
render logs --follow --service <service-name>  # Follow logs in real-time
```

## Quick Deploy Commands

### One-liner deployment:
```bash
# Login and deploy in one go
render login && render services create --from-manifest render.yaml
```

### Deploy with custom name:
```bash
render services create --from-manifest render.yaml --name depHy-chemistry
```

## Troubleshooting

### If deployment fails:
```bash
# Check logs
render logs --service depHy

# Restart service
render restart depHy

# Redeploy
render deploys create --service depHy
```

### If service won't start:
```bash
# Check service status
render services show depHy

# View detailed logs
render logs --service depHy --follow
```

## Your Application URLs

After successful deployment, your app will be available at:
- **Main Site**: `https://depHy.onrender.com`
- **Get Started**: `https://depHy.onrender.com/get-started`
- **API Test**: `https://depHy.onrender.com/api-test`
- **Health Check**: `https://depHy.onrender.com/ping`

## Environment Variables

Your `render.yaml` already includes:
- `FLASK_ENV`: `production`
- `PYTHON_VERSION`: `3.11`

## Next Steps

1. **Deploy**: Run `render services create --from-manifest render.yaml`
2. **Monitor**: Use `render logs --service depHy` to watch the deployment
3. **Test**: Visit your deployed URL to verify everything works
4. **Share**: Your chemistry website is now live! 🧪✨

## Pro Tips

- Use `render logs --follow` to watch logs in real-time during deployment
- The `render.yaml` file makes deployments repeatable and consistent
- You can have multiple environments (staging, production) using different service names
- Render CLI integrates well with CI/CD pipelines

Your depHy chemistry website is ready to go live! 🚀 