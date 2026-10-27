import asyncio
from dotenv import load_dotenv
from ai_client import NewAiClient
from config import Config
from redis_connection import newRedis
from ai_ticket_verifier import ticket_Verifier
from logger import log
load_dotenv()

# main entry point
def main():
    config = Config()
    ticket_verifier = ticket_Verifier(ai_client=NewAiClient(config), redis_c=newRedis(host=config.redis_host, port=config.redis_port, queue=config.queue, logger=log, db=config.redis_db), logger=log, worker_count=config.workers)
    ticket_verifier.start()

    
if __name__ == "__main__":
    main()
