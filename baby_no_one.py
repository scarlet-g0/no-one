from agno.agent import Agent
import google.generativeai as genai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Placeholder for your base class
class Agent:
    def run(self, query: str) -> str:
        raise NotImplementedError

class BabyNoOne(Agent):
    def __init__(self, provider: str = 'google'):
        """
        Initializes the agent for a specific provider.
        Args:
            provider (str): 'google' or 'openai'
        """
        self.provider = provider.lower()
        self.system_prompt = "You are a communication assistant decoding semantic layers from unclear statements."
        
        if self.provider == 'google':
            # --- Google Setup ---
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.client = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=self.system_prompt
            )
            print("🤖 Initialized with Google Gemini")

        elif self.provider == 'openai':
            # --- OpenAI Setup ---
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            print("🤖 Initialized with OpenAI")

        elif self.provider == 'anthropic': #
            print("SCARLET: not implemented")
            #self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            print("🤖 Initialized with Anthropic Claude")

        else:
            raise ValueError("Unsupported provider. Please choose 'google' or 'openai'.")

    def run(self, query: str) -> str:
        if self.provider == 'google':
            # --- Google API Call ---
            response = self.client.generate_content(query)
            return response.text

        elif self.provider == 'openai':
            # --- OpenAI API Call ---
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content

# --- Example of how to use it ---
if __name__ == '__main__':
    # Make sure BOTH GOOGLE_API_KEY and OPENAI_API_KEY are set
    
    print("--- Testing Google Agent ---")
    try:
        google_agent = AgnosticAgent(provider='google')
        google_result = google_agent.run("My manager said 'let's circle back'. What does that mean?")
        print(f"Google's Answer: {google_result}\n")
    except Exception as e:
        print(f"Error with Google Agent: {e}\n")

    print("--- Testing OpenAI Agent ---")
    try:
        openai_agent = AgnosticAgent(provider='openai')
        openai_result = openai_agent.run("My manager said 'let's circle back'. What does that mean?")
        print(f"OpenAI's Answer: {openai_result}")
    except Exception as e:
        print(f"Error with OpenAI Agent: {e}")
