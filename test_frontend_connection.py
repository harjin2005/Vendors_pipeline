import requests
import os
import time

def test_frontend_backend_connection():
    """Test if frontend can connect to backend"""
    # Test different possible backend URLs
    backend_urls = [
        "http://localhost:8000/api",
        "http://backend:8000/api",
        "http://127.0.0.1:8000/api"
    ]
    
    for url in backend_urls:
        try:
            print(f"Testing connection to {url}...")
            response = requests.get(f"{url}/tasks/", timeout=5)
            if response.status_code == 200:
                print(f"✅ SUCCESS: Connected to {url}")
                print(f"Response: {response.json()}")
                return True
            else:
                print(f"❌ FAILED: {url} returned status {response.status_code}")
        except Exception as e:
            print(f"❌ FAILED: Could not connect to {url} - {str(e)}")
    
    return False

if __name__ == "__main__":
    print("Testing frontend-backend connection...")
    success = test_frontend_backend_connection()
    if success:
        print("\n🎉 Connection test passed!")
    else:
        print("\n💥 Connection test failed!")
        print("\nPlease ensure:")
        print("1. The backend service is running on port 8000")
        print("2. Docker containers are properly configured")
        print("3. Network connectivity between services is working")