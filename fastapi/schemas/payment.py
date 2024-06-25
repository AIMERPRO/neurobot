import datetime

from pydantic import BaseModel


class PaymentListSchema(BaseModel):
    id: int
    user_id: int
    uuid: str
    transaction_id: str
    amount: float
    chat_id: str
    days_of_subscription: int
    date: datetime.datetime

    class Config:
        orm_mode = True

