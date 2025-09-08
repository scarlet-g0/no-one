from langfuse.openai import OpenAI as LangfuseOpenAI
import openai as _openai
# Route all openai.OpenAI() constructions to the Langfuse-wrapped client
_openai.OpenAI = LangfuseOpenAI  # noqa: F401

from agno.agent import Agent
import google.generativeai as genai
from openai import OpenAI
import os
import uuid
from dotenv import load_dotenv
from langfuse import get_client, observe

load_dotenv()

# Initialize Langfuse client
langfuse_client = get_client()

# Placeholder for your base class
class Agent:
    def run(self, query: str) -> str:
        raise NotImplementedError

class BabyNoOne(Agent):
    def __init__(self, provider: str = 'google', langfuse_client = None):
        """
        Initializes the agent for a specific provider.
        Args:
            provider (str): 'google' or 'openai'
            langfuse_client: Langfuse client for tracing
        """
        self.provider = provider.lower()
        self.system_prompt = "You are a communication assistant decoding semantic layers from unclear statements."
        self.langfuse_client = langfuse_client
        
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
            # OpenAI client will automatically use Langfuse due to monkey-patching above
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            print("🤖 Initialized with OpenAI")

        elif self.provider == 'anthropic': #
            print("SCARLET: not implemented")
            #self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            print("🤖 Initialized with Anthropic Claude")

        else:
            raise ValueError("Unsupported provider. Please choose 'google' or 'openai'.")

    @observe(name="baby_no_one_run")
    def run(self, query: str) -> str:
        if self.provider == 'google':
            # --- Google API Call ---
            response = self.client.generate_content(query)
            return response.text

        elif self.provider == 'openai':
            # --- OpenAI API Call ---
            # This will be automatically traced by Langfuse due to monkey-patching
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content

@observe(name="run_baby_no_one")
def run_baby_no_one(agent: BabyNoOne, query: str, session_id: str):
    with langfuse_client.start_as_current_span(name="BabyNoOne Chat") as span:
        span.update_trace(session_id=session_id)
        response = agent.run(query)
        
        span.update_trace(
            input=query,
            output=response,
            metadata={'provider': agent.provider, 'system_prompt': agent.system_prompt}
        )
        
        return response

# --- Example of how to use it ---
if __name__ == '__main__':
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    # Test with Google provider
    print("--- Testing Google Agent with Langfuse ---")
    try:
        agent = BabyNoOne(provider='google', langfuse_client=langfuse_client)
        query = "My manager said 'let's circle back'. What does that mean?"
        
        result = run_baby_no_one(agent, query, session_id)
        
        print(f"Agent's response: {result}")
        
    except Exception as e:
        print(f"Error with Google Agent: {e}")
        
    # Flush to ensure data is sent to Langfuse
    langfuse_client.flush()