#!/usr/bin/env python3
"""
depHy Website Startup Script
Launches the API and opens the website
"""

import subprocess
import sys
import os
import time
import webbrowser
import threading

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import pandas
        import numpy
        import sklearn
        import requests
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\nPlease install dependencies first:")
        print("pip3 install -r requirements.txt")
        return False

def start_api():
    """Start the Flask API in a separate thread"""
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nAPI server stopped.")
    except Exception as e:
        print(f"\nError starting API: {e}")

def wait_for_api():
    """Wait for the API to be ready"""
    import requests
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:5001/health", timeout=2)
            if response.status_code == 200:
                print("✓ API is ready!")
                return True
        except:
            pass
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"Waiting for API... ({attempt + 1}/{max_attempts})")
    return False

def main():
    print("=" * 60)
    print("depHy Chemical Reaction Prediction Website")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nStarting depHy API server...")
    print("The API will be available at: http://localhost:5001")
    
    # Start API in background thread
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Wait for API to be ready
    print("Waiting for API to start...")
    if not wait_for_api():
        print("✗ Failed to start API. Please check for errors.")
        sys.exit(1)
    
    # Open website
    print("\nOpening depHy website...")
    website_path = os.path.abspath("index.html")
    webbrowser.open(f"file://{website_path}")
    
    print("\n" + "=" * 60)
    print("depHy is now running!")
    print("=" * 60)
    print("• Website: Open index.html in your browser")
    print("• API: http://localhost:5001")
    print("• Get Started: Click 'Get Started' on the website")
    print("\nPress Ctrl+C to stop the API server")
    print("-" * 60)
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down depHy...")
        print("✓ depHy stopped successfully.")

if __name__ == "__main__":
    main() 