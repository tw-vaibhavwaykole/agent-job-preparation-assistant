from openai import OpenAI
import os
from typing import Dict, List, Optional

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4"

    def generate_interview_tips(self, position: str) -> Dict[str, str]:
        """Generate interview tips for a specific position."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional career advisor helping with job interview preparation."
                    },
                    {
                        "role": "user",
                        "content": f"Generate professional interview tips for a {position} position. Include common questions and best practices."
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return {"tips": response.choices[0].message.content}
        except Exception as e:
            return {"error": str(e)}

    def analyze_resume(self, resume_text: str) -> Dict[str, List[str]]:
        """Analyze resume and provide improvement suggestions."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert resume reviewer."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this resume and provide specific improvement suggestions:\n\n{resume_text}"
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return {"suggestions": response.choices[0].message.content.split('\n')}
        except Exception as e:
            return {"error": str(e)}

    def generate_study_plan(self, topic: str, duration: str) -> Optional[Dict[str, str]]:
        """Generate a personalized study plan."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert education planner."
                    },
                    {
                        "role": "user",
                        "content": f"Create a detailed study plan for {topic} over {duration}."
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return {"plan": response.choices[0].message.content}
        except Exception as e:
            return {"error": str(e)} 