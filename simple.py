import json

from openai import OpenAI
from dotenv import load_dotenv
import os 
from tools import TOOLS,FUNCTION_NAME_TO_FUNCTION_MAP
from utilities.utilities import log 
load_dotenv()

client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
messages=[]

MAX_STEPS=5



messages.append({
    "role":"system",
    "content":"act like a humble agent and response in under  50 words"

    
})
while True:
    user_input=input("\nYOU:")
    messages.append({
        "role":"user",
        "content":user_input
    })
    
    for step in range(MAX_STEPS):
        response=client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
         )
         
        msg=response.choices[0].message
        if not msg.tool_calls:
            break

        log(f"step {step+1}:model requested {len(msg.tool_calls)} tool calls")


        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name=tool_call.function.name
            func_args={}

            try:
                func_args=json.loads(tool_call.function.arguments or "{}")
                log(f"{func_name}({func_args})")
                fn=FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result=fn(**func_args)
            except Exception as e:
                result=f"error while running {func_name}:{e}"
            log(f"{result}")
            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":str(result),
            })

    else:
        fallback="sorry could not finish step limit reached"
        messages.append({
            "role":"assistant",
            "content":fallback

        })
        print("ASSISTANT:" + fallback)
        continue
        
    messages.append({
        "role":"assistant",
        "content":msg.content
    })

    print("ASSISTANT:" + (msg.content or ""))

    