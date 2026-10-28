
from utilities.utilities import log
from datetime import datetime
import json
import requests
def get_current_time():
    return datetime.now()


def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=3"
    response=requests.get(url,timeout=10)
    response.raise_for_status()
    return response.text


TOOLS=[
    {
        "type":"get_current_time",
        "function":{
            "name":"get_current_time",
            "description":"return the current date and time  ",
            "parameters":{
                "type":"object",
                "properties":{}

            },
        },
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"returns the current date and time for a given city ",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get the weather for",
                    }

                },
                "required":["city"]
            }
        }
    }
]  
FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time":get_current_time,
    "get_city_weather":get_city_weather
}

def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}

    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f"🔧 {func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
        result = fn(**func_args)
    except Exception as e:
        result = f"Error while running {func_name} : {e}"

    log(f"   ↳ {result}")
    return str(result)
