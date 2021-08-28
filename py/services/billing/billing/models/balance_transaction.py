import enum

from marshmallow_enum import EnumField
from sqlalchemy.sql import func

from billing.extensions import db, marshmallow

__all__ = ["BalanceTransaction"]


class BalanceTransactionType(enum.Enum):
    charge = "charge"
    payment = "payment"
    payment_refund = "payment_refund"


class BalanceTransactionStatus(enum.Enum):
    available = "available"
    pending = "pending"


class BalanceTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    type = db.Column(db.Enum(BalanceTransactionType), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(
        db.Enum(BalanceTransactionStatus), nullable=False
    )

    updated_at = db.Column(db.DateTime, server_default=func.now())
    created_at = db.Column(db.DateTime, server_onupdate=func.now())

    def __repr__(self):
        return f"<BalanceTransaction {self.id}: {self.account_id}>"


class BalanceTransactionSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = BalanceTransaction
        include_fk = True

    type = EnumField(BalanceTransactionType, by_value=True)
    status = EnumField(BalanceTransactionStatus, by_value=True)


balance_transaction_schema = BalanceTransactionSchema()
balance_transactions_schema = BalanceTransactionSchema(many=True)
