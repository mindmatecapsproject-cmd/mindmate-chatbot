from fastapi import FastAPI
from pydantic import BaseModel
from stress_analyzer import stress_analyzer

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):

    stress_level, confidence, context = (
        stress_analyzer.analyze_message(request.message)
    )

    return {
        "response": "MindMate received your message.",
        "stress_level": stress_level,
        "confidence_score": confidence,
        "stress_context": context
    }
