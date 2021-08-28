from hamcrest import assert_that, equal_to, has_entries

from pytest_toolbelt import matchers


def test_balance_transactions_create(client, account):
    response = client.post(
        "/balance_transactions/", json={"account_id": account["id"], "type": "charge", "amount": 100, "currency": "USD"}
    )

    assert_that(response, matchers.has_status(201))

    response = client.get(f'/accounts/{account["id"]}/')

    assert_that(response, matchers.has_status(200))
    assert_that(
        response.data.decode(),
        matchers.is_json(has_entries(balance=equal_to(100))),
    )
