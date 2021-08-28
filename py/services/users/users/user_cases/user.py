from talepy import run_transaction

from users.exception import NoSuchUser
from users.extensions import db
from users.models.user import User
from users.sagas.auth import IssueAccessToken
from users.sagas.billing import CreateAccount
from users.sagas.user import CreateUser, SendUserRegistered


def register_user_use_case(email, first_name, last_name, phone=None, password=None):
    state = run_transaction(
        steps=[CreateUser(), CreateAccount(), IssueAccessToken(), SendUserRegistered()],
        starting_state={
            "email": email,
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        },
    )

    return state["user"], state["access_token"]


def get_user_use_case(user_id):
    user = db.session.query(User).filter(User.id == user_id).one_or_none()

    NoSuchUser.require_condition(user, "The user with {user_id} identifier does not exist", user_id=user_id)

    return user


def update_user_use_case(user_id, **kwargs):
    with db.session.begin(subtransactions=True):
        user = get_user_use_case(user_id)

        for k, v in kwargs.items():
            setattr(user, k, v)

        db.session.add(user)

    return user
