import random

from hamcrest import assert_that

import pytest

from pytest_toolbelt import matchers


@pytest.fixture()
def user_id():
    return random.randint(1, 10000)


@pytest.fixture()
def account(client, user_id):
    response = client.post("/accounts/", json={"user_id": user_id})

    assert_that(response, matchers.has_status(201))

    return response.json
