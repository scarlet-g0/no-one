from agno.agent import Agent
from openai import OpenAI
import os

class BabyNoOne(Agent):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = "You are a communication assistant decoding semantic layers from unclear statements."

    def run(self, query: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
