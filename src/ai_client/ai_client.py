from openai import OpenAI
import os 
from config import Config
from ai_client import Response


class AiClient:
    def __init__(self, config: Config) -> None:
        self.api_key = config.api_key
        self.base_url = config.base_url
        try:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except Exception as e:
            print(e)
            
    def makeRequest(self, prompt: str) -> str|None:
        try:
            print("Start ai ")
            reply = self.client.beta.chat.completions.parse(
               model="gemini-3.5-flash-lite",
                   messages=[
                       {   "role": "system",
                           "content": "You are a helpful assistant. that verifies if email content is valid. it must have a url normal question/support question and personal info answer if valid or not"
                       },
                       {
                           "role": "user",
                           "content": prompt
                       }
                   ],
                   response_format=Response,
                   reasoning_effort="medium",)
           
            return reply.choices[0].message.content
           
        except Exception as e:
            print(e)



def NewAiClient(config: Config) -> AiClient:
    return AiClient(config)