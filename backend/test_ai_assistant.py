"""
Test AI Assistant with local analysis
"""
import requests

BASE_URL = "http://localhost:8000"

# Login as owner
print("Logging in as owner...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "owner@canteen.com", "password": "owner123"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"[OK] Login successful!\n")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test various queries
    test_queries = [
        "What is the peak hour?",
        "Which day has highest sales?",
        "Show me top 5 items",
        "Which items cause wastage?",
        "What should I prepare tomorrow?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Q: {query}")
        print(f"{'='*60}")
        
        response = requests.post(
            f"{BASE_URL}/ai/query",
            headers=headers,
            json={"query": query}
        )
        
        if response.status_code == 200:
            answer = response.json()["response"]
            print(answer)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        print()
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
