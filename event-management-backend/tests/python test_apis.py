import requests
import json

base_url = "http://localhost:8000"

# Test 1: Get all events
response = requests.get(f"{base_url}/events/")
print("Events:", response.status_code, json.dumps(response.json()[:1], indent=2))

# Test 2: Get venues
response = requests.get(f"{base_url}/venues/")
print("Venues:", response.status_code)

# Test 3: Get participants
response = requests.get(f"{base_url}/participants/")
print("Participants:", response.status_code)

# Test 4: Get leaderboard
response = requests.get(f"{base_url}/scores/leaderboard")
print("Leaderboard:", response.status_code)