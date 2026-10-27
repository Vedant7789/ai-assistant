import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS

load_dotenv()
client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
stream=client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[{"role":"user","content":"tell me the weather of pune and weathe rof delhi"}],
    tools=TOOLS,
    stream=True,
)
full_response=""

for chunk in stream:
    if not chunk.choices:
        continue
    delta=chunk.choices[0].delta
    if delta.tool_calls:
        print(delta.tool_calls,end="",flush=True)
        