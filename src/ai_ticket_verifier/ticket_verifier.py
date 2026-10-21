import asyncio
from ai_client import AiClient
from redis_connection import redisC

class ticket_Verifier():
    def __init__(self, ai_client: AiClient, redis_c: redisC, worker_count) -> None:
        self.ai_client = ai_client
        self.redis_c = redis_c
        self.worker_count = worker_count

    async def start(self):

        #handle queue logic
        # while True: 
            # ticket = self.redis_c.pull_from_Queue()

            print('ticket verifier started')
            results = await asyncio.gather(*(self.ai_client.makeRequest(prompt="this is a test lollll bruh") for _ in  range(self.worker_count)))
            print(results)
