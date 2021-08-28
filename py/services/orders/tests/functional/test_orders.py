from hamcrest import assert_that, equal_to, has_entries
from pytest_toolbelt import matchers

from orders import settings


def test_orders_create(client, user_id, user_jwt_payload, requests_mock):
    requests_mock.get(settings.BILLING_URL + f"/accounts/find_by_user_id/{user_id}/", json={"id": 1})
    requests_mock.post(settings.BILLING_URL + f"/balance_transactions/", json={"id": 1})

    response = client.post(
        "/orders/",
        json={"items": [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 2}]},
        headers={"X-JWT-Payload": user_jwt_payload},
    )

    assert_that(response, matchers.has_status(201))
    assert_that(
        response.data.decode(),
        matchers.is_json(has_entries(amount=equal_to(300))),
    )
