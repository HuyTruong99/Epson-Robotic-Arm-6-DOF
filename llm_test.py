

from openai import OpenAI

client = OpenAI()

print("Testing LLM...")

response = client.responses.create(
    model="gpt-5.6-sol",
    input="""
You are a command interpreter for an Epson robot arm.

Allowed commands:
MOVE_X_50
MOVE_X_10
POS
STOP

Convert the user's instruction into exactly ONE allowed command.

User instruction:
Move the robot 50 mm in X.

Return only the command.
"""
)

print("LLM response:", response.output_text)
