import os
import asyncio
from dotenv import load_dotenv
from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI,
    OpenAIChatCompletionsModel, 
    set_default_openai_client, 
    function_tool,
    set_tracing_disabled, 
    set_default_openai_api,
    handoff )

# 🚫 Disable tracing for clean output (optional for beginners)
set_tracing_disabled(disabled=True)

# 🌿 Load environment variables from .env file
load_dotenv()

#   1) Environment & Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
set_default_openai_api("chat_completions")

##   Initialize the AsyncOpenAI-compatible client with Gemini details
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

#  2) Global Model Initialization
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",        # ⚡ Fast Gemini model
    openai_client=external_client
)

billing_agent = Agent(name="Billing Agent", instructions="Handle billing questions.")
refund_agent  = Agent(name="Refund agent",  instructions="Handle refunds.")

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Help the user with their questions. "
        "If they ask about billing, handoff to the Billing agent. "
        "If they ask about refunds, handoff to the Refund agent."
    ),
    handoffs=[billing_agent, handoff(refund_agent)],
)

async def main():
    result = await Runner.run(triage_agent, "I need to check my refund status of 500 dollars.")
    print(result.final_output)
