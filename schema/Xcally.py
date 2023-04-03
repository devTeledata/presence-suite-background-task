from pydantic import BaseModel
from typing import Optional

from schema.XcallyAgent import XcallyAgent
from schema.XcallyContact import XcallyContact

class Xcally(BaseModel):
    chat_id: Optional[str] = None
    id: str
    OpenchannelAccountId: str
    OpenchannelInteractionId: str
    UserId: Optional[str] = None
    ContactId: str
    body: str
    contact: XcallyContact
    agent: XcallyAgent