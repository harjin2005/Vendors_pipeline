#!/usr/bin/env python3
"""
Script to run both the Django backend and Streamlit frontend locally
"""

import subprocess
import sys
import time
import threading
import os

def run_backend():
    """Run the Django backend server"""
    print("Starting Django backend server...")
    try:
        # Run Django migrations first
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        
        # Start the Django development server
        subprocess.run([sys.executable, "manage.py", "runserver", "8000"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running backend: {e}")
        return False
    return True

def run_frontend():
    """Run the Streamlit frontend"""
    print("Starting Streamlit frontend...")
    try:
        # Set the API URL for local development
        env = os.environ.copy()
        env["STREAMLIT_SERVER_PORT"] = "8501"
        
        # Try to run streamlit with the current Python interpreter
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                "frontend/app.py", 
                "--server.port=8501", 
                "--server.address=localhost"
            ], env=env, check=True)
        except subprocess.CalledProcessError:
            # If that fails, try with python -m streamlit
            subprocess.run([
                "streamlit", "run", 
                "frontend/app.py", 
                "--server.port=8501", 
                "--server.address=localhost"
            ], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running frontend: {e}")
        return False
    return True

def main():
    print("🚀 Starting Vendor Pipeline System Locally")
    print("=" * 50)
    
    # Update the secrets.toml for local development
    secrets_path = "frontend/.streamlit/secrets.toml"
    if os.path.exists(secrets_path):
        with open(secrets_path, "w") as f:
            f.write('API_BASE_URL = "http://localhost:8000/api"\n')
        print("✅ Updated secrets.toml for local development")
    
    print("\n📝 Instructions:")
    print("1. Backend will run on: http://localhost:8000")
    print("2. Frontend will run on: http://localhost:8501")
    print("3. Press Ctrl+C to stop both services")
    print("\n⏳ Starting services...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Give backend some time to start
    time.sleep(5)
    
    # Start frontend in main thread
    run_frontend()
    
    print("\n🛑 Services stopped")

if __name__ == "__main__":
    main()