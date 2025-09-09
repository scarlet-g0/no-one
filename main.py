from baby_no_one import BabyNoOne, langfuse_client, run_baby_no_one
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

if __name__ == "__main__":
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    # Initialize the agent with Langfuse client
    agent = BabyNoOne(provider='google', langfuse_client=langfuse_client)
    
    query = "My new girlfriend said: `It feels like rainy days being with you.` She loves the weather and she was smiling when she said it . I am confused."
    
    # Use the traced function to run the agent
    result = run_baby_no_one(agent, query, session_id)
    
    print(f"Agent's response: {result}")
    print(f"Session ID: {session_id}")
    
    # Flush to ensure data is sent to Langfuse
    langfuse_client.flush()
