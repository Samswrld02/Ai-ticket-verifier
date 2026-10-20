from pydantic import BaseModel

class Response(BaseModel):
    name: str
    date: str
    content:list[str]