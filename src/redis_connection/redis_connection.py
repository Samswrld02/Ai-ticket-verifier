from redis import Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import ConnectionError, TimeoutError
import redis
import time
from threading import Event
from logger import log
from logging import Logger
from queue import Queue, Full
from model import Ticket, ValidationError


retry = Retry(ExponentialBackoff(), 8)

# variables gotton from config class
def newRedis(host, port, queue, logger: Logger, db) -> redisC :
    r = redis.Redis(host=host, port=port, db=db ,decode_responses=True, socket_keepalive=True, retry_on_error=[ConnectionError, TimeoutError], retry=retry)

    return redisC(redis=r, queue=queue, logger=logger)


class redisC():
    def __init__(self, redis: Redis, queue, logger: Logger) -> None:
        self.r = redis
        self.queue = queue
        self.internalQueue = Queue[str](150)
        self.logger = logger 
    
    def read_into_Queue(self, event: Event):
            while not event.is_set():
                try:
                    # pop the value
                    result = self.r.blpop(self.queue, timeout=2)
                    if not result:
                        continue
                    while not event.is_set():
                        # try pushing it into internal queue
                        try:
                            _, data = result
                            self.internalQueue.put(str(data), block=True, timeout=2)
                            break
                        # if full exception thrown by queue continue loop aka retry pushing into queue
                        except Full:
                            time.sleep(1)
                            continue
                # connection error
                except ConnectionError as e:
                    self.logger.error(e)
                    time.sleep(1)

        
                    
                    
                        

         
