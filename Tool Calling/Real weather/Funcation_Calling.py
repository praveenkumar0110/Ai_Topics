import json
import requests
from openai import OpenAI

# 🔗 Connect to Ollama (NOT OpenAI cloud) -------------------------------------1
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# 🌦️ Real weather tool function  LLM just name ketkum: get_weather oru funcation 
def get_weather(city: str):
    url = f"http://api.weatherapi.com/v1/current.json?key=93c2cc79bea8437cbb752525263001&q={city}&aqi=no"
    res = requests.get(url)
    return res.json()

# intha function ah josn ah llm ulla load pannrom
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 👤 User input
city = input("Enter city name: ")
# role llm 
messages = [
    {"role": "user", "content": f"What is the current weather in {city}?"}
]
 #prepare the prompt messages ----------------------------------------------2 epo promt ah model ku send pannum 
response = client.chat.completions.create( 
    model="qwen2.5",
    messages=messages, # intha mesaage tha llm roles---- like user, system, assistant la vechitu use pannum
    tools=tools,
)

msg = response.choices[0].message  #llm replay enna kuduthuruku ?


# 🔍 Check tool call
if msg.tool_calls:
    tool_call = msg.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments) # dict la convert pannum --------------  

    print("Tool called with:", arguments)

    # 🔨 Execute real function
    result = get_weather(arguments["city"])
    print("Weather API result:", result)

    # 🔁 Send result back to LLM ------appen llm back
    messages.append(msg)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id, 
        "content": json.dumps(result)
    })
    #user weather kekkuraan… en kitta weather illa… aana get_weather nu oru tool irukku… adha use pannalaam"
# final response from llm with tool result ----------------------------------3
    final = client.chat.completions.create(
        model="qwen2.5",
        messages=messages,
    )

    print("\nFinal Answer:\n")
    print(final.choices[0].message.content) #  user promt and system promt oda final answer display pannum

else:
    print("LLM did not call the tool. Response:")
    print(msg.content)
