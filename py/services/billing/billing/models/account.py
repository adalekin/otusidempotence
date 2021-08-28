from sqlalchemy.sql import func

from billing.extensions import db, marshmallow

__all__ = ["Account"]


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    balance = db.Column(db.Integer, server_default="0", nullable=False)

    updated_at = db.Column(db.DateTime, server_default=func.now())
    created_at = db.Column(db.DateTime, server_onupdate=func.now())

    def __repr__(self):
        return f"<Account {self.id}: {self.user_id}>"


class AccountSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Account


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
