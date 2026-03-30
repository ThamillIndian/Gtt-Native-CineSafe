import os
import json
from typing import Dict, Any, Optional
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model: str = None):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model or os.getenv("MODEL_NAME", "gemini-2.5-flash")

    def generate_text(self, prompt: str, system_message: str = "You are a helpful assistant.") -> str:
        # For Gemini 3, we use the new generate_content API
        # We can also leverage thinking_level for better reasoning
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"{system_message}\n\n{prompt}",
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )
        return response.text

    def generate_json(self, prompt: str, system_message: str = "You are a helpful assistant. Always return valid JSON.") -> Dict[str, Any]:
        content = self.generate_text(prompt, system_message)
        try:
            # Simple cleanup for JSON blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from LLM response: {e}")
            print(f"Content: {content}")
            return {}

# Singleton instance
default_client = LLMClient()
