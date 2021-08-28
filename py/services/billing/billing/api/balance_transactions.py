from billing.models.balance_transaction import balance_transaction_schema
from billing.use_cases.balance_transaction import balance_transaction_use_case


def create(balance_transaction):
    balance_transaction_ = balance_transaction_use_case(**balance_transaction)

    return balance_transaction_schema.dump(balance_transaction_), 201
