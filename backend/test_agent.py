from backend.agent.agent import create_agent

agent = create_agent()

response = agent.run(
    "What is the demand forecast for Field & Stream Sportsman 16 Gun Fire Safe?"
)

print(response)