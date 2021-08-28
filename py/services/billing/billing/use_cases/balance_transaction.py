from billing.exception import NoSuchAccount
from billing.extensions import db
from billing.models.account import Account
from billing.models.balance_transaction import (
    BalanceTransaction,
    BalanceTransactionStatus,
)


def balance_transaction_use_case(account_id, type, amount, currency):
    with db.session.begin(subtransactions=True):
        account_ = db.session.query(Account).filter(Account.id == account_id).one_or_none()

        NoSuchAccount.require_condition(
            account_, "The account {account_id} does not exist", account_id=account_id
        )

        balance_transaction_ = BalanceTransaction(status=BalanceTransactionStatus.available, account_id=account_id, type=type, amount=amount, currency=currency)

        # FIXME: currency exchange rate
        account_.balance = account_.balance + balance_transaction_.amount

        db.session.add(account_)
        db.session.add(balance_transaction_)

    return balance_transaction_
