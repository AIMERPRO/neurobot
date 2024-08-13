import datetime
from typing import List

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from database.connect import connect_db, disconnect_db
from database.models import User, Payment, Transaction
from schemas.payment import PaymentListSchema
from schemas.transaction import TransactiontListSchema
from schemas.user import UserListSchema

app = FastAPI()

origins = ["*",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    app.add_event_handler("startup", connect_db)
    app.add_event_handler("shutdown", disconnect_db)


@app.get("/transaction/approve/")
async def approve_transaction(MNT_TRANSACTION_ID: str, MNT_OPERATION_ID: str, MNT_AMOUNT: float, MNT_SUBSCRIBER_ID: str):
    # days_of_subscription = 30

    # if 300 <= amount <= 320:
    #     days_of_subscription = 1
    #
    # elif 1000 <= amount <= 1020:
    #     days_of_subscription = 7
    #
    # elif 3000 <= amount <= 3020:
    #     days_of_subscription = 30

    if MNT_AMOUNT == 1:
        days_of_subscription = 1

    elif MNT_AMOUNT == 2:
        days_of_subscription = 7

    elif MNT_AMOUNT == 3:
        days_of_subscription = 30

    if days_of_subscription:
        transaction = await Transaction.create(transaction_id=MNT_TRANSACTION_ID, operation_id=MNT_OPERATION_ID, amount=MNT_AMOUNT, chat_id=MNT_SUBSCRIBER_ID,
                                  days_of_subscription=days_of_subscription)

        payment = await Payment.query.where(Payment.transaction_id == MNT_OPERATION_ID).gino.all()[-1]
        await payment.update(paid=True).apply()

        if payment.paid:
            user = await User.query.where(User.chat_id == MNT_SUBSCRIBER_ID).gino.first()
            subscribe_end = datetime.datetime.now() + datetime.timedelta(days=days_of_subscription)
            await user.update(subscribe_end=subscribe_end).apply()

        return transaction.to_dict()

    else:
        return {'status': 'Invalid amount'}


@app.get("/users/", response_model=List[UserListSchema])
async def get_users():
    users = await User.query.gino.all()

    return users


@app.get("/payments/", response_model=List[PaymentListSchema])
async def get_payments():
    payments = await Payment.query.gino.all()

    return payments


@app.get("/transactions/", response_model=List[TransactiontListSchema])
async def get_transactions():
    transactions = await Transaction.query.gino.all()

    return transactions
