import requests
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Hugging Face API details
API_KEY = "key_here"  # Replace with your actual key
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Request model
class ChatRequest(BaseModel):
    user_input: str

# Function to communicate with Hugging Face API
def generate_response(user_input: str):
    payload = {"inputs": user_input}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error {response.status_code}: {response.text}"

# API route
@app.post("/chat")
def chat(request: ChatRequest):
    ai_response = generate_response(request.user_input)
    return {"response": ai_response}

# Run the server (if running as a script)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
