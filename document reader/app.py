    
import ollama
import os
import smtplib
from email.message import EmailMessage
from unstructured.partition.auto import partition
from PyPDF2 import PdfReader

SENDER_EMAIL = "ipraveen.e@gmail.com" 
APP_PASSWORD = "vqxdphucjngaxdxl"    


def list_files_tool(folder_path: str):
    try:
        files = os.listdir(folder_path)
        return {"files": files}
    except Exception as e:
        return f"Error: {str(e)}"

def read_document_tool(file_path: str):
    try:
        elements = partition(filename=file_path)
        content = "\n\n".join([str(el) for el in elements])
        if not content.strip(): return "The document is empty."
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def send_email_tool(recipient: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return f" Email sent successfully to {recipient}!"
    except Exception as e:
        return f" Failed: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files_tool",
            "description": "Lists files in a folder.",
            "parameters": {"type": "object", "properties": {"folder_path": {"type": "string"}}, "required": ["folder_path"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_document_tool",
            "description": "Reads document content.",
            "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email_tool",
            "description": "Sends an email summary to the boss.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string", "description": "The detailed 5-10 line summary of the document."}
                },
                "required": ["recipient", "subject", "body"]
            }
        }
    }
]

messages = [
    {
        "role": "system", 
        "content": (
            "You are a tool-calling assistant. NEVER generate Python code blocks.\n"
            "STRICT WORKFLOW:\n"
            "1. Call 'read_document_tool' to get the file content.\n"
            "2. STOP and wait for the file content to be returned.\n"
            "3. Once you have the content, write a detailed 10-line summary.\n"
            "4. ONLY THEN, call 'send_email_tool' with a professional 'subject' and the summary as 'body'.\n"
            "5. If the user mentions an email, use it. Otherwise use ipraveen.e@gmail.com."
        )
    }
]


while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]: break

    messages.append({"role": "user", "content": user_input})
    

    response = ollama.chat(model="llama3.1", messages=messages, tools=tools)
    # print(type(response)) 

    while response['message'].get('tool_calls'):

        messages.append(response['message']) 
        
        # print(messages)
        for tool in response['message']['tool_calls']:
            name = tool['function']['name']
            
            args = tool['function']['arguments']
            
            print(f"Tool execution: {name}...")
            
            if name == "list_files_tool": result = list_files_tool(args['folder_path'])
            elif name == "read_document_tool": result = read_document_tool(args['file_path'])
            elif name == "send_email_tool": result = send_email_tool(args['recipient'], args['subject'], args['body'])


            messages.append({"role": "tool", "content": str(result), "name": name})


        response = ollama.chat(model="llama3.1", messages=messages, tools=tools)


    print(f"\nAI: {response['message']['content']}")

