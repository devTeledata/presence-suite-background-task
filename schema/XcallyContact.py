from pydantic import BaseModel
from typing import Optional


class XcallyContact(BaseModel):
    id: str
    firstName: str
    phone: Optional[str] = None
    email: Optional[str] = None