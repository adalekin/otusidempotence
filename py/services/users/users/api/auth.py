import connexion

from users.models.user import user_schema
from users.user_cases.auth import login_use_case, logout_use_case

from . import utils


def login(login):
    user, access_token = login_use_case(**login)

    user_dump = user_schema.dump(user)
    user_dump["access_token"] = access_token

    return user_dump, 200


def logout():
    access_token, _ = utils.jwt_read_from_header(request=connexion.request)
    logout_use_case(access_token)

    return connexion.NoContent, 204
