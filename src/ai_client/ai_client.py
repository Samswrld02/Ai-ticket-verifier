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
                          "content": """You are an AI ticket verifier for a professional helpdesk. Your task is to review incoming support tickets for clarity, completeness, and validity (no spam/nonsense).
                                        Here is the ticket you need to evaluate:
                                        - Type
                                        - Subject
                                        - Body
                                        - Requester

                                        Evaluate the ticket based on the following criteria:
                                        1. **Clarity:** Is the problem or question described clearly?
                                        2. **Completeness:** Does the message contain enough context for a support agent to get started? (Note: A URL or link is NEVER mandatory, unless it explicitly concerns a broken web page. Never penalize the absence of a URL unless the context requires it).
                                        3. **Validity:** Is this a serious support request or is it obvious spam/nonsense?"""
                        
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