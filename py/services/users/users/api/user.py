import connexion

from users.exception import AccessDenied
from users.models.user import user_schema
from users.user_cases.user import get_user_use_case, register_user_use_case, update_user_use_case

from . import utils


def create(user):
    user_, access_token = register_user_use_case(**user)

    user_dump = user_schema.dump(user_)
    user_dump["access_token"] = access_token

    return user_dump, 201


def get_current():
    _, payload = utils.jwt_read_from_header(request=connexion.request)
    AccessDenied.require_condition(payload, "Access denied")

    return get(user_id=payload["user_id"])


def get(user_id):
    user = get_user_use_case(user_id)

    return user_schema.dump(user)


def update_current(user1):
    _, payload = utils.jwt_read_from_header(request=connexion.request)
    AccessDenied.require_condition(payload, "Access denied")

    return update(user_id=payload["user_id"], user1=user1)


def update(user_id, user1):
    user = update_user_use_case(user_id=user_id, **user1)

    return user_schema.dump(user)
