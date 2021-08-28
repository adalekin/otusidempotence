import connexion
from billing.exception import AccessDenied
from billing.models.account import account_schema
from billing.use_cases.account import (
    create_account_use_case,
    delete_account_use_case,
    get_account_by_user_id_use_case,
    get_account_use_case,
)

from . import utils


def create(account):
    account_ = create_account_use_case(**account)

    return account_schema.dump(account_), 201


def get_current():
    _, payload = utils.jwt_read_from_header(request=connexion.request)
    AccessDenied.require_condition(payload, "Access denied")

    return get_by_user_id(user_id=payload["user_id"])


def get_by_user_id(user_id):
    account = get_account_by_user_id_use_case(user_id=user_id)

    return account_schema.dump(account), 200


def get(account_id):
    account = get_account_use_case(account_id=account_id)

    return account_schema.dump(account), 200


def delete(account_id):
    delete_account_use_case(account_id=account_id)

    return connexion.NoContent, 204
