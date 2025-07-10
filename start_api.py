#!/usr/bin/env python3
"""
depHy Reaction Prediction API Startup Script
"""

import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import pandas
        import numpy
        import sklearn
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\nPlease install dependencies first:")
        print("pip install -r requirements.txt")
        return False

def main():
    print("=" * 50)
    print("depHy Reaction Prediction API")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nStarting the API server...")
    print("The API will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nAPI server stopped.")
    except Exception as e:
        print(f"\nError starting API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("[depHy] Attempting to start the API server...")
    try:
        proc = subprocess.Popen([sys.executable, "app.py"])
        print("[depHy] API server process started (PID: {}), waiting for server to be ready...".format(proc.pid))
        # Wait a few seconds for the server to start
        for i in range(10):
            time.sleep(1)
            try:
                import requests
                r = requests.get("http://localhost:5001/ping", timeout=1)
                if r.ok:
                    print("[depHy] API is up and responding at http://localhost:5001")
                    break
            except Exception as e:
                print(f"[depHy] Waiting for API... ({i+1}/10)")
        else:
            print("[depHy] API did not respond after 10 seconds. Check app.py for errors.")
    except Exception as e:
        print(f"[depHy] Failed to start API: {e}") 