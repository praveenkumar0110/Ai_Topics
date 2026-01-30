import json
import re
import requests
from openai import OpenAI

# 🔗 Connect to Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# 🛠️ YouTube search tool (no API, regex method)
def youtube_search(query: str):
    url = f"https://www.youtube.com/results?search_query={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers).text

    # Extract video IDs
    video_ids = list(set(re.findall(r"watch\?v=(\S{11})", res)))

    videos = []
    for vid in video_ids[:5]:
        videos.append({
            "title": f"https://www.youtube.com/watch?v={vid}",
            "url": f"https://www.youtube.com/watch?v={vid}"
        })

    return videos


# 🧠 Tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "youtube_search",
            "description": "Search YouTube videos by query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

# 👤 User input
query = input("What videos you want to search? ")

messages = [
    {"role": "user", "content": f"Search YouTube for: {query}"}
]

# 🧠 First LLM call
response = client.chat.completions.create(
    model="qwen2.5",
    messages=messages,
    tools=tools,
    temperature=0
)

msg = response.choices[0].message


if msg.tool_calls:
    tool_call = msg.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    print("Tool called with:", args)

   
    results = youtube_search(args["query"])

    
    messages.append(msg)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(results)
    })

    final = client.chat.completions.create(
        model="qwen2.5",
        messages=messages,
    )

    print("\nTop YouTube Videos:\n")
    print(final.choices[0].message.content)

else:
    print("LLM did not call tool:")
    print(msg.content)
