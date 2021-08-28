from hamcrest import assert_that, equal_to, has_entries

from pytest_toolbelt import matchers


def test_accounts_create(client):
    response = client.post("/accounts/", json={"user_id": 1})

    assert_that(response, matchers.has_status(201))
    assert_that(
        response.data.decode(),
        matchers.is_json(has_entries(balance=equal_to(0))),
    )

    response = client.post("/accounts/", json={"user_id": 1})
    assert_that(response, matchers.has_status(400))


def test_accounts_delete(client, account):
    response = client.delete(f'/accounts/{account["id"]}/')

    assert_that(response, matchers.has_status(204))
