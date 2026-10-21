import os

#config class for variables need by program
class Config:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", default="defaultkey")
        self.base_url = os.getenv("API_BASE_URL", default="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.redis_host = os.getenv("REDIS_HOST", default="localhost")
        self.redis_port = os.getenv("REDIS_PORT", default=6379)
        self.queue = os.getenv("REDIS_QUEUE", default="ticket:events")



