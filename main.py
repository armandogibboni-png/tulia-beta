from fastapi import FastAPI
from pydantic import BaseModel
import os
import random
import json

app = FastAPI()

# ===== INPUT =====
class ChatInput(BaseModel):
    input: str

class FeedbackInput(BaseModel):
    score: int


# ===== LANGUAGE =====
def is_italian(text):
    words = ["non", "sono", "confuso", "stanco"]
    return any(w in text.lower() for w in words)


# ===== RESPONSE =====
def generate_response(text):
    if is_italian(text):
        return "Sembra che ci sia qualcosa che pesa un po’… vuoi restare un attimo su questo?"
    
    return "It sounds like something might be weighing on you a bit… would you like to stay with it for a moment?"


# ===== CHAT =====
@app.post("/chat")
def chat(data: ChatInput):

    response = generate_response(data.input)

    return {
        "response": response,
        "show_feedback": random.random() < 0.3
    }


# ===== FEEDBACK =====
@app.post("/feedback")
def feedback(data: FeedbackInput):

    with open("feedback.json", "a") as f:
        f.write(json.dumps({"score": data.score}) + "\n")

    return {"status": "ok"}


# ===== ENTRYPOINT =====
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run("main:app", host="0.0.0.0", port=port)