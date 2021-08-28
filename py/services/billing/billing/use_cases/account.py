from billing.extensions import db
from billing.models.account import Account
from billing.exception import AlreadyExists, NoSuchAccount


def create_account_use_case(user_id):
    with db.session.begin(subtransactions=True):
        account_already_exists = db.session.query(Account.query.filter(Account.user_id == user_id).exists()).scalar()

        AlreadyExists.require_condition(
            not account_already_exists, "An account already exists with the specified user identifier"
        )

        account_ = Account(user_id=user_id)
        db.session.add(account_)

    return account_


def get_account_use_case(account_id):
    account = db.session.query(Account).filter(Account.id == account_id).one_or_none()

    NoSuchAccount.require_condition(account, "The account {account_id} does not exist", account_id=account_id)

    return account


def get_account_by_user_id_use_case(user_id):
    account = db.session.query(Account).filter(Account.user_id == user_id).one_or_none()

    NoSuchAccount.require_condition(account, "The account for user {user_id} does not exist", user_id=user_id)

    return account


def delete_account_use_case(account_id):
    with db.session.begin(subtransactions=True):
        account = db.session.query(Account).filter(Account.id == account_id).one_or_none()

        NoSuchAccount.require_condition(account, "The account {account_id} does not exist", account_id=account_id)

        db.session.delete(account)

    return account
