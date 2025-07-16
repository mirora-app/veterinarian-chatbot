from pydantic import BaseModel
from fastapi import FastAPI
import json
import requests

from connections import GROQ_ENDPOINT, MODEL, USE_LOCAL, build_prompt, headers
from pricing_data import pricing_data

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    user_message = req.message

    if USE_LOCAL:
        payload = {
            "prompt": build_prompt(user_message),
            "temperature": 0.3,
            "max_tokens": 512
        }
    else:
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful veterinary assistant."},
                {"role": "user", "content": build_prompt(user_message)}
            ],
            "temperature": 0.3
        }

    try:
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
