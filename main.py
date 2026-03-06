from fastapi import FastAPI
from models.schema import IdeaInput
from services.ai_service import analyze_startup_idea

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Startup Validator API is running"}


@app.post("/analyze")
def analyze(data: IdeaInput):

    ai_result = analyze_startup_idea(data.idea)

    return {
        "startup_idea": data.idea,
        "ai_analysis": ai_result
    }