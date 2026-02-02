import os
import json
import requests
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"



def read_policy():
    with open("privacy_policy.txt", "r", encoding="utf-8") as f:
        return f.read()


def send_email(to, subject, body):
    gmail = os.getenv("GMAIL")
    pwd = os.getenv("APP_PASSWORD")

    msg = EmailMessage()
    msg["From"] = gmail
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail, pwd)
        server.send_message(msg)

    return "✅ Email Sent Successfully!"


def ask_ollama(prompt):
    res = requests.post(
        OLLAMA_URL,
        json={"model": "llama3", "prompt": prompt, "stream": False},
    )
    return res.json()["response"]

'''
User wants wishes mail
Boss email policy la irukku
I must send_email
JSON format kudu
LLM output:

{
 "action": "send_email",
 "to": "ipraveen.e@gmail.com",
 "subject": "...",
 "body": "..."
}
'''
#extract_json() = LLM output la irundhu tool call data clean-a edukkura filter
def extract_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]

  
# step 1 ------------------------------------------ main la funcation run 
def run_agent(user_input):
    policy = read_policy()

    prompt = f"""
You are a STRICT AI Email Agent.

Use the company data to find boss email.

Company Data:
{policy}  

User Request:
{user_input}

Reply ONLY in JSON:

{{
 "action": "send_email",
 "to": "...",
 "subject": "...",
 "body": "..."
}}
"""

    output = ask_ollama(prompt)
 
    data = json.loads(extract_json(output))

    if data["action"] == "send_email":
        return send_email(data["to"], data["subject"], data["body"])

    return "No action needed."


if __name__ == "__main__":
    while True:
        q = input("Email Information : ")
        print("Agent:", run_agent(q))
