from hamcrest import *

from pytest_toolbelt import matchers


def test_jwks(client):
    response = client.get("/jwks/")

    assert_that(response, matchers.has_status(200))
    assert_that(
        response.data.decode(),
        matchers.is_json(has_key("keys")),
    )
