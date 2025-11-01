import asyncio
from dataclasses import dataclass

from agents import (
    Agent, Runner, AsyncOpenAI, RunContextWrapper, function_tool,
    set_default_openai_client, set_default_openai_api, set_tracing_disabled,
    SQLiteSession,)

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

# A tool function that accesses local context via the wrapper
@function_tool
def add_function(a: int, b: int) -> int:
    return a + b

async def main():
    # Create your context object

    # Define an agent that will use the tool above
    agent = Agent(  
        name="Assistant",
        tools=[add_function],
        model="gemini-2.5-flash",
        instructions="You are a helpful assistant that adds two numbers provided in the context.",
        
    )

    # Create session memory
    #session = SQLiteSession("my_first_conversation")

    print("=== First Turn with Memory ===")

    # Turn1
    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="What is the sum of the two numbers 2 and 3?",
        max_output_tokens=1024,
    )


    print(result.final_output)  # Expected output: The user John is 47 years old.
    print("*"*20)
    print(result.to_input_list())


if __name__ == "__main__":
    asyncio.run(main())