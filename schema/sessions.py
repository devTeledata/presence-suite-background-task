from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Session(BaseModel):
    id: str
    last_interations = datetime.now()
    operator_request: bool = False
    account_unlock: bool = False
    reset_password: bool = False
    account: str = None
    messages: list = []
    questions: list = None

    def dict(self):
        return {
            "_id": self.id,
            "last_interations": self.last_interations,
            "operator_request": self.operator_request,
            "account_unlock": self.account_unlock,
            "reset_password": self.reset_password,
            "account": self.account,
            "messages": self.messages,
            "questions": self.questions,
        }