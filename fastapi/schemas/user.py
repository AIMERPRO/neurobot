from pydantic import BaseModel


class UserListSchema(BaseModel):
    id: int
    name: str
    username: str
    chat_id: str

    class Config:
        orm_mode = True

