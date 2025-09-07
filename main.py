from baby_no_one import BabyNoOne
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    agent = BabyNoOne()
    query = "My manager told me my project now has 'high visibility'."
    result = agent.run(query)
    print(f"Agent's response: {result}")
