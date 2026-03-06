import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def analyze_startup_idea(idea: str):

    prompt = f"""
Analyze the following startup idea:

{idea}

Return ONLY valid JSON.

JSON structure:

{{
 "category": "startup category",
 "similar_startups": ["startup1","startup2","startup3"],
 "viability_score": number between 0-100,
 "difficulty": "Easy or Medium or Hard",

 "idea_scores": {{
  "market_potential": number 1-10,
  "competition_level": number 1-10,
  "technical_complexity": number 1-10,
  "investment_required": "Low or Medium or High"
 }},

 "suggestions": ["suggestion1","suggestion2","suggestion3"]
}}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    if "choices" not in result:
        return {"error": "AI API error", "api_response": result}

    ai_text = result["choices"][0]["message"]["content"]

    cleaned_text = re.sub(r"```json|```", "", ai_text).strip()

    try:
        ai_json = json.loads(cleaned_text)
    except json.JSONDecodeError:
        ai_json = {
            "warning": "AI response not valid JSON",
            "raw_output": cleaned_text
        }

    return ai_json