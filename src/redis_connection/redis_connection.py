from redis import Redis
import redis



#variables gotton from config class
def newRedis(host, port, queue) -> redisC :
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    return redisC(redis=r, queue=queue)


class redisC():
    def __init__(self, redis: Redis, queue) -> None:
        self.r = redis
        self.queue = queue
    
    def pull_from_Queue(self) -> None:
        self.r.blpop(self.queue)

    def handle(self) -> None:
        pass
