from pydantic import BaseModel


class TransactiontListSchema(BaseModel):
    id: int
    user_id: int
    transaction_id: str
    operation_id: str
    amount: float
    days_of_subscription: int
    chat_id: str

    class Config:
        orm_mode = True
