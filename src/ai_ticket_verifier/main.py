import asyncio
from openai import OpenAI
import dotenv
from ai_client import aiclient, Response

async def startWorker():
    try:
        response = aiclient.beta.chat.completions.parse(
    model="gemini-3.5-flash-lite",
    messages=[
        {   "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "whats my name what date is it lol"
        }
    ],
    response_format=Response,
    reasoning_effort="low",
)
        print(response.choices[0].message.parsed)

    except Exception as e:
        print(e)

    

if __name__ == "__main__":
    asyncio.run(startWorker()) 
