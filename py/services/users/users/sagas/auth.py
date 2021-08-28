import datetime

import requests
from talepy.steps import Step

from users import settings
from users.exception import AuthFailure
from users.extensions import db
from users.models.user import User

AUTH_SESSION = requests.Session()


def _auth_api(path):
    return settings.AUTH_URL + path


class IssueAccessToken(Step):
    def execute(self, state):
        response = AUTH_SESSION.post(
            _auth_api("/jwt/encode/"), json={"iss": "trymarqet", "sub": "users", "payload": {"user_id": state["user"].id}}
        )
        response.raise_for_status()

        state["access_token"] = response.json()["access_token"]
        return state

    def compensate(self, state):
        response = AUTH_SESSION.post(_auth_api("/jwt/blacklist/"), json={"access_token": state["access_token"]})
        response.raise_for_status()


class RevokeAccessToken(Step):
    def execute(self, state):
        response = AUTH_SESSION.post(_auth_api("/jwt/blacklist/"), json={"access_token": state["access_token"]})
        response.raise_for_status()
        return state

    def compensate(self, state):
        # TODO: exclude the access token from the blacklist
        pass


class Authenticate(Step):
    def execute(self, state):
        with db.session.begin(subtransactions=True):
            user = db.session.query(User).filter(User.email == state["email"]).one_or_none()

            AuthFailure.require_condition(
                user and user.verify_password(state["password"]), "The email or password is incorrect"
            )

            state["previous_last_login"] = user.last_login

            user.last_login = datetime.datetime.utcnow()
            db.session.add(user)

        state["user"] = user
        return state

    def compensate(self, state):
        user = state["user"]

        with db.session.begin(subtransactions=True):
            user.last_login = state["previous_last_login"]
            db.session.add(user)
