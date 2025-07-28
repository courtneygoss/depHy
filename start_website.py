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
    print("[depHy] Attempting to start the API server...")
    try:
        proc = subprocess.Popen([sys.executable, "app.py"])
        print("[depHy] API server process started (PID: {}), waiting for server to be ready...".format(proc.pid))
        for i in range(10):
            time.sleep(1)
            try:
                import requests
                r = requests.get("http://localhost:5001/ping", timeout=1)
                if r.ok:
                    print("[depHy] API is up and responding at http://localhost:5001")
                    return proc
            except Exception as e:
                print(f"[depHy] Waiting for API... ({i+1}/10)")
        else:
            print("[depHy] API did not respond after 10 seconds. Check app.py for errors.")
    except Exception as e:
        print(f"[depHy] Failed to start API: {e}")
    return None

def start_website():
    print("[depHy] Starting website server at http://localhost:8000 ...")
    try:
        subprocess.run([sys.executable, "-m", "http.server", "8000"], check=True)
    except Exception as e:
        print(f"[depHy] Failed to start website server: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Start depHy API and/or website server.")
    parser.add_argument('--api', action='store_true', help='Start only the API server')
    parser.add_argument('--website', action='store_true', help='Start only the website server')
    parser.add_argument('--both', action='store_true', help='Start both API and website (default)')
    args = parser.parse_args()

    if args.api:
        start_api()
    elif args.website:
        start_website()
    else:
        # Default: start both
        api_proc = start_api()
        print("[depHy] Launching website server in 2 seconds...")
        time.sleep(2)
        start_website()
        if api_proc:
            print("[depHy] Shutting down API server...")
            api_proc.terminate() 