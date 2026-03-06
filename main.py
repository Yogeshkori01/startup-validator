from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI(title="AI Startup Validator API")


# Enable CORS so frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Schema
class StartupIdea(BaseModel):
    idea: str


@app.get("/")
def home():
    return {"message": "AI Startup Validator API is running"}


@app.post("/analyze")
def analyze_idea(data: StartupIdea):

    idea = data.idea

    prompt = f"""
You are an expert startup analyst.

Analyze the following startup idea and return JSON only.

Startup Idea: {idea}

Return response strictly in JSON format:

{{
"category": "",
"similar_startups": [],
"viability_score": "",
"difficulty": "",
"suggestions": []
}}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(url, headers=headers, json=payload)

        result = response.json()

        ai_output = result["choices"][0]["message"]["content"]

        import json
        import re

        # Remove markdown formatting if present
        cleaned = re.sub(r"```json|```", "", ai_output).strip()

        analysis = json.loads(cleaned)

        return {
            "startup_idea": idea,
            "ai_analysis": analysis
        }

    except Exception as e:

        return {
            "error": str(e)
        }