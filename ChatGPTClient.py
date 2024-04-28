import requests
import json
import os

api_key = os.getenv('OPENAI_API_KEY')

class ChatGPTClient:
    def __init__(self):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def ask_question(self, prompt, model="gpt-3.5-turbo", max_tokens=150):
        """
        Send a prompt to the ChatGPT API and return the generated response.
        """
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        })
        response = requests.post(self.endpoint, headers=self.headers, data=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}, {response.text}"