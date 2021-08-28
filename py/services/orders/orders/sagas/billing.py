import requests
from talepy.steps import Step

from orders import settings

BILLING_SESSION = requests.Session()


def _billing_api(path):
    return settings.BILLING_URL + path


class GetAccount(Step):
    def execute(self, state):
        response = BILLING_SESSION.get(_billing_api(f'/accounts/find_by_user_id/{state["user_id"]}/'))
        response.raise_for_status()

        state["account_id"] = response.json()["id"]
        return state

    def compensate(self, state):
        pass


class CreatePayment(Step):
    def execute(self, state):
        response = BILLING_SESSION.post(
            _billing_api("/balance_transactions/"),
            json={
                "account_id": state["account_id"],
                "type": "payment",
                "amount": state["order"].amount,
                "currency": "USD",
            },
        )
        response.raise_for_status()

        state["balance_transaction_id"] = response.json()["id"]
        return state

    def compensate(self, state):
        response = BILLING_SESSION.post(
            _billing_api("/balance_transactions/"),
            json={
                "account_id": state["account_id"],
                "type": "payment_refund",
                "amount": state["order"].amount,
                "currency": "USD",
            },
        )
        response.raise_for_status()
