import ollama
import json
import io
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']



def get_drive_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)



def read_drive_file_tool(file_name: str):

    service = get_drive_service()
    
 
    search_term = file_name.replace('.txt', '').replace('_', ' ').strip() 
    
    queries = [
        f"name = '{search_term}'", 
        f"name contains '{search_term}'", 
        f"name contains '{search_term.split()[0]}'" 
    ]

    items = []
    for q in queries:
        try:
            results = service.files().list(q=q, fields="files(id, name, mimeType)").execute()
            items = results.get('files', [])
            if items: break  
        except Exception:
            continue

    if not items:
        return {"error": f"Could not find a file named '{file_name}' or similar to '{search_term}'."}


    file_id = items[0]['id']
    mime_type = items[0]['mimeType']
    actual_name = items[0]['name']
    fh = io.BytesIO()

    try:
        
        if mime_type == 'application/vnd.google-apps.document':
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
            request = service.files().export_media(fileId=file_id, mimeType='text/csv')
        else:
            request = service.files().get_media(fileId=file_id)

        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        content = fh.getvalue().decode("utf-8", errors='ignore') 
        
        return {
            "content": content, 
            "actual_filename": actual_name
        }
    except Exception as e:
        return {"error": f"Failed to access {actual_name}: {str(e)}"}

        

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_drive_file_tool",
            "description": "Reads text content from a Google Drive file by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The filename (e.g., 'Ai Topics' or 'Email Accounts Data')."
                    }
                },
                "required": ["file_name"]
            }
        }
    }
]



system_prompt = """
You are a Google Drive Assistant.
RULES:
1. Use 'read_drive_file_tool' for EVERY file-related question.
2. Based on your image, filenames are likely 'Ai Topics', 'Email Accounts Data', 'XL Topic's', etc. 
3. DO NOT add .txt or .doc to filenames unless the user says so.
4. Your final response MUST be exactly 8 to 9 lines long.
5. Be professional and clear. No JSON or code in the final answer. 
"""

messages = [{"role": "system", "content": system_prompt}]

print("Example: 'Summarize Ai Topics' or 'What is in Email Accounts Data?'")


while True:
    user_input = input("\nAsk: ")
    if user_input.lower() in ['exit', 'quit']: break

    messages.append({"role": "user", "content": user_input})


    response = ollama.chat(model="qwen2.5:3b", messages=messages, tools=tools)

    if response['message'].get('tool_calls'):
        for tool in response['message']['tool_calls']:
            args = tool['function']['arguments']
                    
            if isinstance(args, str): args = json.loads(args)
            
            print(f" 🔍 Searching Drive for: {args.get('file_name')}...")
            result = read_drive_file_tool(**args)

        
            messages.append(response['message'])
            messages.append({"role": "tool", "content": json.dumps(result)})

        
        response = ollama.chat(model="qwen2.5:3b", messages=messages)

    print("\n📄 Summary:\n")
    print(response['message']['content'])
    