import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def analyze_startup_idea(idea: str):

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
- Scores must follow the ranges defined above
- Do NOT return markdown
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

        response = requests.post(url, headers=headers, json=payload, timeout=60)

        result = response.json()

        if "choices" not in result:
            return {
                "error": "AI API error",
                "api_response": result
            }

        ai_text = result["choices"][0]["message"]["content"]

        cleaned_text = re.sub(r"```json|```", "", ai_text).strip()

        json_match = re.search(r"\{.*\}", cleaned_text, re.DOTALL)

        if json_match:
            cleaned_text = json_match.group()

        ai_json = json.loads(cleaned_text)

    except Exception as e:

        return {
            "error": "Failed to process AI response",
            "details": str(e)
        }


    # ---------- Validation ----------

    if not ai_json.get("similar_startups"):
        ai_json["similar_startups"] = [
            "Market competitor analysis required",
            "Industry research recommended",
            "Startup ecosystem exploration suggested"
        ]

    if not ai_json.get("suggestions"):
        ai_json["suggestions"] = [
            "Validate idea with real users",
            "Conduct market research",
            "Develop an MVP before scaling"
        ]


    # Ensure idea_scores exists
    if "idea_scores" not in ai_json:
        ai_json["idea_scores"] = {}

    scores = ai_json["idea_scores"]


    # Validate individual score fields

    if "market_potential" not in scores:
        scores["market_potential"] = 5

    if "competition_level" not in scores:
        scores["competition_level"] = 5

    if "technical_complexity" not in scores:
        scores["technical_complexity"] = 5

    if "investment_required" not in scores:
        scores["investment_required"] = "Medium"


    ai_json["idea_scores"] = scores


    return ai_json