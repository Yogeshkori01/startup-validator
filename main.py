from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI(title="AI Startup Validator API")


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
You are an expert startup analyst and venture capitalist.

Analyze the following startup idea carefully.

Startup Idea:
{idea}

Return ONLY valid JSON using this structure:

{{
 "category": "startup category",

 "similar_startups": [
  "Startup1",
  "Startup2",
  "Startup3"
 ],

 "viability_score": number between 0-100,

 "difficulty": "Easy or Medium or Hard",

 "idea_scores": {{
  "market_potential": number between 1-10,
  "competition_level": number between 1-10,
  "technical_complexity": number between 1-10,
  "investment_required": "Low or Medium or High"
 }},

 "suggestions": [
  "Suggestion 1",
  "Suggestion 2",
  "Suggestion 3"
 ]
}}

Rules:
- Always provide at least 3 similar startups
- Always provide at least 3 suggestions
- Return JSON only
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat",
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

        # Remove markdown formatting
        cleaned = re.sub(r"```json|```", "", ai_output).strip()

        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)

        if json_match:
            cleaned = json_match.group()

        analysis = json.loads(cleaned)

        # ---------- Validation ----------

        if "idea_scores" not in analysis:
            analysis["idea_scores"] = {}

        scores = analysis["idea_scores"]

        scores.setdefault("market_potential", 5)
        scores.setdefault("competition_level", 5)
        scores.setdefault("technical_complexity", 5)
        scores.setdefault("investment_required", "Medium")

        analysis.setdefault("similar_startups", [])
        analysis.setdefault("suggestions", [])

        return {
            "startup_idea": idea,
            "ai_analysis": analysis
        }

    except Exception as e:

        return {
            "error": str(e)
        }