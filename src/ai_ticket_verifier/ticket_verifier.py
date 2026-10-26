from threading import Thread
import threading
from ai_client import AiClient
from redis_connection import redisC
import signal, sys

class ticket_Verifier():
    def __init__(self, ai_client: AiClient, redis_c: redisC, worker_count) -> None:
        self.ai_client = ai_client
        self.redis_c = redis_c
        self.worker_count = worker_count
        self._stop = threading.Event()
        self.threads: list[Thread] = []

    def start(self):
        signal.signal(signal.SIGINT, self.on_signal)   # Ctrl+C
        signal.signal(signal.SIGTERM, self.on_signal) # kill

        #handle queue logic
        print('ticket verifier started')

        # one reader
        reader = Thread(target=self.reader, args=(self._stop,), daemon=True)
        reader.start()

        # workers specified in .env
        for _ in range(self.worker_count):
            t = Thread(target=self.worker, daemon=True)
            t.start()
            self.threads.append(t)

        # event to stop verifier
        self._stop.wait()

    # worker method
    def worker(self):
        while True:
            try:
                result  = self.redis_c.internalQueue.get(block=True)
                if result == "STOP":
                    break

                # process result 
                print(self.ai_client.makeRequest(prompt=result))
            finally:
                self.redis_c.internalQueue.task_done()

    # reader method
    def reader(self, event: threading.Event):
        while not event.is_set():
            self.redis_c.read_into_Queue()

    # handles exit logic 
    def on_signal(self, signum, frame):
        try:
            print("starting exit of ticket_verifier")
            for _ in range(self.worker_count):
                self.redis_c.internalQueue.put("STOP")
            for t in self.threads:
                t.join()
            self._stop.set()
        except Exception as e:
            print(e)
        sys.exit(0)
        


