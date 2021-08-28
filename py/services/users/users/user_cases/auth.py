from talepy import run_transaction

from users.sagas.auth import Authenticate, IssueAccessToken, RevokeAccessToken


def login_use_case(email, password):
    state = run_transaction(
        steps=[Authenticate(), IssueAccessToken()], starting_state={"email": email, "password": password}
    )

    return state["user"], state["access_token"]


def logout_use_case(access_token):
    run_transaction(
        steps=[RevokeAccessToken()], starting_state={"access_token": access_token}
    )
