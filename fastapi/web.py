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
async def approve_transaction(transaction_id: str, operation_id: str, amount: float, chat_id: str):
    return {"transaction_id": transaction_id, "operation_id": operation_id, "amount": amount, "chat_id": chat_id}


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
