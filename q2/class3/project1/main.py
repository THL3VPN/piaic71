from agents import Agent, Runner
from dotenv import load_dotenv

clie

agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "hello")

print(result.final_output)