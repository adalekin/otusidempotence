import requests
from talepy.steps import Step

from users import settings

BILLING_SESSION = requests.Session()


def _billing_api(path):
    return settings.BILLING_URL + path


class CreateAccount(Step):
    def execute(self, state):
        response = BILLING_SESSION.post(_billing_api("/accounts/"), json={"user_id": state["user"].id})
        response.raise_for_status()

        state["account_id"] = response.json()["id"]
        return state

    def compensate(self, state):
        response = BILLING_SESSION.delete(_billing_api(f'/accounts/{state["account_id"]}/'))
        response.raise_for_status()
