from utils.ai import build_insight_prompt, call_gemini_api

# Agent implementation scaffold for AI-powered insight generation using Gemini.
# This module interacts with the Gemini API to generate narrative insights and recommendations.


def generate_business_insights(statistics: dict) -> dict:
    prompt = build_insight_prompt(statistics)
    insights = call_gemini_api(prompt)

    return {
        "prompt": prompt,
        "insights": insights,
    }
