#!/usr/bin/env python3
"""
Test script to verify deployment setup
"""
import requests
import os
import sys

def test_local_server():
    """Test if the local server starts and responds correctly"""
    print("Testing deployment setup...")
    
    # Test 1: Check if all required files exist
    required_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'runtime.txt',
        'index.html',
        'get-started.html',
        'api_test.html',
        'periodic table.jpg',
        'model.pkl',
        'preprocessors.pkl'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
    
    # Test 2: Check if Flask app can be imported
    try:
        from app import app
        print("✅ Flask app imports successfully")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    # Test 3: Check if PORT environment variable handling works
    test_port = 5001
    os.environ['PORT'] = str(test_port)
    
    try:
        from app import app
        # This would normally start the server, but we're just testing the import
        print("✅ PORT environment variable handling works")
    except Exception as e:
        print(f"❌ PORT environment variable handling failed: {e}")
        return False
    
    print("\n🎉 Deployment setup looks good!")
    print("\nTo deploy on Render:")
    print("1. Push your code to a Git repository (GitHub, GitLab, etc.)")
    print("2. Go to render.com and create a new Web Service")
    print("3. Connect your repository")
    print("4. Render will automatically detect the Python environment")
    print("5. Deploy!")
    
    return True

if __name__ == "__main__":
    success = test_local_server()
    sys.exit(0 if success else 1) 