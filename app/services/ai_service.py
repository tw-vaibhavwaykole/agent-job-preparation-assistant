from typing import Dict, List, Optional
import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

async def analyze_content(content: str) -> Dict:
    """Analyze content using OpenAI GPT"""
    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Analyze this study material and provide difficulty level (1-5), estimated reading time in minutes, and key topics."},
                {"role": "user", "content": content}
            ]
        )
        # Parse the response
        analysis = response.choices[0].message.content
        # TODO: Parse the analysis into structured data
        return {
            "difficulty_level": 3.0,  # placeholder
            "estimated_time": 30,     # placeholder
            "tags": ["topic1", "topic2"]  # placeholder
        }
    except Exception as e:
        print(f"Error analyzing content: {e}")
        return {
            "difficulty_level": 1.0,
            "estimated_time": 10,
            "tags": []
        }

async def generate_summary(content: str) -> str:
    """Generate a summary of the content"""
    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Create a concise summary of this study material."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "" 