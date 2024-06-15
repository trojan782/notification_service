from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    events: list = [ "all" ] # Have users subcribed to a default event list

class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.isoformat())
    message: str



