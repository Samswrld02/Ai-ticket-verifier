from pydantic import BaseModel, Field

class Response(BaseModel):
    name: str
    date: str
    support_question:list[str]
    url: str
    valid: bool = Field(description="answer true or false if all email is deemed valid")
    Reason: str = Field(description="give a short summaray why validation failed or passed, max 2 sentences")