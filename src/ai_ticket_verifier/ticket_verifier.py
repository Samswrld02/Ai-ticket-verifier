from threading import Thread
import threading
from ai_client import AiClient
from redis_connection import redisC
import signal, sys
from logging import Logger
from model import Ticket, ValidationError

class ticket_Verifier():
    def __init__(self, ai_client: AiClient, redis_c: redisC, worker_count, logger: Logger) -> None:
        self.ai_client = ai_client
        self.redis_c = redis_c
        self.logger = logger
        self.worker_count = worker_count
        self._stop = threading.Event()
        self.threads: list[Thread] = []

    def start(self):
        signal.signal(signal.SIGINT, self.on_signal)   # Ctrl+C
        signal.signal(signal.SIGTERM, self.on_signal) # kill

        # handle queue logic
        self.logger.info("ticket verifier started")

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

                # signal worker to stop close
                if result == "STOP":
                    break

                # validate data itself, skip data if validation fails
                ticket = self.validate_data(result)
                if not ticket:
                    self.logger.error("validation failed incorrect ticket")
                    continue

                # process result note: will be changed to business logic later -> sent back to redis queue
                print(self.ai_client.makeRequest(prompt=result))
            except Exception as e:
                self.logger.error(e)
            finally:
                self.redis_c.internalQueue.task_done()

    # reader method
    def reader(self, event: threading.Event):
        # while not event.is_set():
            try: 
                self.redis_c.read_into_Queue(event=event)
            except Exception as e:
                self.logger.error(e)

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

    # method for validating incoming data
    def validate_data(self, json_data: bytes|str) -> Ticket|bool:
        try:
            return Ticket.model_validate_json(json_data)
        except ValidationError as e:
            return False

    # method for sending structured response to redis
    def handle_response(self) -> None:
        pass


