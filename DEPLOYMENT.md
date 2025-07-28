# Deployment Guide for depHy Chemistry Website

## Overview
This guide will help you deploy your depHy chemistry website on Render.com.

## Prerequisites
- A Git repository (GitHub, GitLab, etc.) with your code
- A Render.com account

## Files Required for Deployment
✅ All required files are present in your project:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `Procfile` - Process definition
- `runtime.txt` - Python version specification
- HTML files (`index.html`, `get-started.html`, `api_test.html`)
- Static assets (`periodic table.jpg`)
- ML models (`model.pkl`, `preprocessors.pkl`)

## Step-by-Step Deployment Instructions

### 1. Prepare Your Repository
```bash
# Make sure all files are committed to your Git repository
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Deploy on Render

1. **Go to Render.com**
   - Visit [render.com](https://render.com)
   - Sign up or log in to your account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"

3. **Connect Your Repository**
   - Connect your Git repository (GitHub, GitLab, etc.)
   - Select the repository containing your depHy project

4. **Configure the Service**
   - **Name**: `depHy` (or your preferred name)
   - **Environment**: `Python`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

5. **Environment Variables** (Optional)
   - `FLASK_ENV`: `production`
   - `PYTHON_VERSION`: `3.11`

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### 3. Verify Deployment

After deployment, your application will be available at:
`https://your-app-name.onrender.com`

Test the following endpoints:
- **Homepage**: `https://your-app-name.onrender.com/`
- **Get Started**: `https://your-app-name.onrender.com/get-started`
- **API Test**: `https://your-app-name.onrender.com/api-test`
- **Health Check**: `https://your-app-name.onrender.com/ping`
- **API Endpoint**: `https://your-app-name.onrender.com/predict-reaction`

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version in `runtime.txt` is correct

2. **App Won't Start**
   - Verify the `Procfile` is correct
   - Check that `app.py` has the correct Flask app instance

3. **Static Files Not Loading**
   - Ensure all HTML files and images are in the root directory
   - Check that routes are properly configured in `app.py`

4. **ML Models Not Loading**
   - Verify `model.pkl` and `preprocessors.pkl` are included in your repository
   - Check file paths in `app.py`

### Testing Locally

Before deploying, test locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the test script
python test_deployment.py

# Start the server locally
python app.py
```

## Features Deployed

✅ **Web Interface**: Beautiful chemistry website with modern UI
✅ **API Endpoints**: RESTful API for reaction prediction
✅ **Static File Serving**: HTML pages and images
✅ **ML Integration**: Pre-trained models for chemistry predictions
✅ **Health Checks**: `/ping` endpoint for monitoring
✅ **CORS Support**: Cross-origin requests enabled

## Support

If you encounter issues:
1. Check the Render logs in your dashboard
2. Verify all files are committed to your repository
3. Test locally first using `python test_deployment.py`
4. Ensure your Git repository is public or Render has access

Your depHy chemistry website is now ready for deployment! 🧪✨ 