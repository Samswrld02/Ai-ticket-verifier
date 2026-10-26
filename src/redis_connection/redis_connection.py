from redis import Redis
import redis
from queue import Queue

#variables gotton from config class
def newRedis(host, port, queue) -> redisC :
    r = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_keepalive=True)

    return redisC(redis=r, queue=queue)


class redisC():
    def __init__(self, redis: Redis, queue) -> None:
        self.r = redis
        self.queue = queue
        self.internalQueue = Queue(150)
    
    def read_into_Queue(self):
        result = self.r.blpop(self.queue)
        if result:
            queue_name, data = result
            self.internalQueue.put(str(data), block=True, timeout=2)
        
    def handle(self) -> None:
        pass
