from pydantic import BaseModel, ConfigDict, ValidationError

class Ticket(BaseModel):
    model_config = ConfigDict(strict=True)

    type: str
    ticket_id: str
    ticket_number: str
    subject: str
    body: str
    requester: str
    created_by: str|None

