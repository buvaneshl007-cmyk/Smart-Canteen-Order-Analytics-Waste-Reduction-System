"""
Test script to verify analytics endpoints are working
"""
import requests

BASE_URL = "http://localhost:8000"

# Login as owner
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "owner@canteen.com", "password": "owner123"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"[OK] Login successful, token: {token[:20]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test analytics endpoints
    endpoints = [
        "/analytics/daily?days=7",
        "/analytics/weekly",
        "/analytics/time",
        "/analytics/items"
    ]
    
    for endpoint in endpoints:
        print(f"\n--- Testing {endpoint} ---")
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Data length: {len(data)}")
            if data:
                print(f"Sample: {data[0]}")
        else:
            print(f"Error: {response.text}")
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
