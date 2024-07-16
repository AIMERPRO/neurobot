from datetime import datetime

from database.connect import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    chat_id = db.Column(db.String)
    subscribe_end = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User(name={self.name})>"


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uuid = db.Column(db.String)
    transaction_id = db.Column(db.String)
    amount = db.Column(db.Float)
    chat_id = db.Column(db.String)
    days_of_subscription = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now())
    paid = db.Column(db.Boolean, default=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transaction_id = db.Column(db.String)
    operation_id = db.Column(db.String)
    amount = db.Column(db.Float)
    days_of_subscription = db.Column(db.Integer)
    chat_id = db.Column(db.String)
