from pydantic import BaseModel
from typing import Optional


class XcallyAgent(BaseModel):
    id: str
    name: str
    fullname: Optional[str] = None