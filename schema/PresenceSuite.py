from pydantic import BaseModel
from typing import Optional


class PresenceSuite(BaseModel):
    chat_id: Optional[str] = None
    space_id: str
    email: str
    name: str
