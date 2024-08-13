from datetime import datetime

from pydantic import BaseModel


class UserListSchema(BaseModel):
    id: int
    name: str
    username: str
    chat_id: str
    subscribe_end: datetime

    class Config:
        orm_mode = True

