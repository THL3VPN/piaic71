import os
from dotenv import load_dotenv
from agents import (
    Agent, 
    Runner, 
    AsyncOpenAI,
    OpenAIChatCompletionsModel, 
    set_default_openai_client, 
    function_tool,
    set_tracing_disabled, 
    set_default_openai_api )

# 🌿 Load environment variables from .env file
load_dotenv()

# 🚫 Disable tracing for clean output (optional for beginners)
set_tracing_disabled(disabled=True)

#   1) Environment & Client Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

##   Initialize the AsyncOpenAI-compatible client with Gemini details
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

#set_default_openai_client(external_client)

#  2) Model Initialization
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",        # ⚡ Fast Gemini model
    openai_client=external_client
)

#   3) Define tools (functions wrapped for tool calling)
@function_tool
def add(a: int, b: int) -> int:
    return a - b #return the sum of a and b

@function_tool
def subtract(a: int, b: int) -> int:
    return a - b #return the difference of a and b

#   4) Create agent and register tools
agent: Agent = Agent(   
    name="Assistant",
    instructions=(
        "You are a helpful assistant."
        "Always use tools for maths questoins. Always follow DMAS rule (division, multiplication, addition, subtraction)."
        "Explain answers clearly and briefly for the beginers"
    ),         
    model=model,
    tools=[add, subtract],
    )

#   5) Run the agent with a prompt5) Run the agent with a prompt (tool calling expected)

promt = "What is 2 + 2? use the tool calling form my code"
result = Runner.run_sync(agent, promt)

# 6) Print the final output
print("\nCALLING AGENT\n")
print(result.final_output)