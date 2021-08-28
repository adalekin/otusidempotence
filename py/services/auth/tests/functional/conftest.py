from hamcrest import *

import pytest

from pytest_toolbelt import matchers


@pytest.fixture(scope="session")
def access_token(client):
    response = client.post("/jwt/encode/", json={"iss": "test", "sub": "test", "payload": {"user_id": 1}})
    assert_that(response, matchers.has_status(200))

    return response.json["access_token"]
