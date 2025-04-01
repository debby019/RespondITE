import requests

test_url = "http://127.0.0.1:8000/chat"
test_data = {"user_input": "What can you do?"}

response = requests.post(test_url, json=test_data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
