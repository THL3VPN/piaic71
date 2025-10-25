import asyncio
from dataclasses import dataclass

from agents import (
    Agent, Runner, AsyncOpenAI, RunContextWrapper, function_tool,
    set_default_openai_client, set_default_openai_api, set_tracing_disabled,)

from dotenv import load_dotenv
import os

load_dotenv()

api_key_gemini = os.getenv("GEMINI_API_KEY")
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=api_key_gemini,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_default_openai_client(external_client)


# Define a simple context using a dataclass
@dataclass
class UserInfo:  
    name: str
    uid: int

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    # Create your context object
    user_info = UserInfo(name="John", uid=123)  

    # Define an agent that will use the tool above
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
        model="gemini-2.5-flash"
    )

    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )


    print(result.final_output)  # Expected output: The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())