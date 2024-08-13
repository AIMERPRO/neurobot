from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserListSchema(BaseModel):
    id: int
    name: str
    username: str
    chat_id: str
    subscribe_end: Optional[datetime] = None

    class Config:
        orm_mode = True

