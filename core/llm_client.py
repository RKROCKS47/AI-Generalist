# core/llm_client.py
import os
from typing import List, Dict, Any

from openai import OpenAI


class LLMClient:
    def __init__(self, model: str):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat_json(self, system: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Enforce JSON-only output through response_format.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}] + messages,
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        content = response.choices[0].message.content
        # OpenAI guarantees valid JSON when using response_format
        import json

        return json.loads(content)
