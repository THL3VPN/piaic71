from agents import (
    Agent, Runner, AsyncOpenAI, 
    set_default_openai_client, set_default_openai_api, set_tracing_disabled, 
    handoff,enable_verbose_stdout_logging)
from dotenv import load_dotenv
import os

load_dotenv()
#enable_verbose_stdout_logging()

api_key_gemini = os.getenv("GEMINI_API_KEY")
set_default_openai_api("chat_completions")
set_tracing_disabled(True)


external_client = AsyncOpenAI(
    api_key=api_key_gemini,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_default_openai_client(external_client)

math_agent: Agent = Agent(
    name="math_agent", 
    instructions=("""You are a math agent. You can only answer math question. 
                  After answering the question return back to the triage_agent"""),
    model="gemini-2.5-flash")

history_agent: Agent = Agent(
    name="history_agent", 
    instructions="You are a history agent. You can only answer history questions",
    model="gemini-2.5-flash")
    

triage_agent: Agent = Agent(
    name="Assistant", 
    instructions=(
        """You are a manager agent, You can call math_agent or history_agent as handoffs. 
        Once the agent is called get the control back to the main triage agent as the last agent."""),
    model="gemini-2.5-flash",
    handoffs=[math_agent, history_agent])



result = Runner.run_sync(triage_agent, "what is 2+2 ?")
print(result.last_agent.name)
print(result.final_output)
