"""
Minimal ChatGPT wrapper
"""

import json
import uuid

import requests

BASE_URL = "https://chatgpt.duti.tech/"

class GPT:
    def __init__(self, config) -> None:
        self.config = config
        self.session = requests.Session()
        if not "access_token" in config:
            raise Exception("GPT: Access token not provided")
        
        self.session.headers.clear()
        self.session.headers.update(
            {
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {config['access_token']}",
                "Content-Type": "application/json",
                "X-Openai-Assistant-App-Id": "",
                "Connection": "close",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://chat.openai.com/chat",
            },
        )

    def __is_valid(self, data: dict) -> bool:
        try:
            data["message"]["content"]
        except TypeError or KeyError:
            return False
        return True
     
    def send(self, prompt: str):
        parent_id = str(uuid.uuid4())
        data = {
            "action": "next",
            "messages": [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": {"content_type": "text", "parts": [prompt]},
                },
            ],
            "conversation_id": None,
            "parent_message_id": parent_id,
            "model": "text-davinci-002-render-sha"
        }
        
        response = self.session.post(
            url=BASE_URL + "api/conversation",
            data=json.dumps(data),
            timeout=360,
            stream=True
        )
        if response.status_code != 200:
            raise Exception(f"GPT: Response {response.status_code}: {response.text}")
        
        for line in response.iter_lines():
            line = str(line)[2:-1]
            if line == "" or line is None: continue
            if "data: " in line: line = line[6:]
            if line == "[DONE]": break

            line = line.replace('\\"', '"').replace("\\'", "'").replace("\\\\", "\\")
            try: line = json.loads(line)
            except json.decoder.JSONDecodeError: continue
            
            if not self.__is_valid(line):
                raise Exception(f"GPT: Field missing: {line}")
            
            message = line["message"]["content"]["parts"][0]
            conversation_id = line["conversation_id"]
            parent_id = line["message"]["id"]
            
            yield {
                "message": message,
                "conversation_id": conversation_id,
                "parent_id": parent_id,
            }
