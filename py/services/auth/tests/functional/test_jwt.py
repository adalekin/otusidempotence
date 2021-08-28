from hamcrest import *

from pytest_toolbelt import matchers


def test_jwt_encode(client):
    response = client.post("/jwt/encode/", json={"iss": "test", "sub": "test", "payload": {"user_id": 123}})
    assert_that(response, matchers.has_status(200))


def test_jwt_blacklist(client, access_token):
    response = client.post("/jwt/blacklist/", json={"access_token": access_token})
    assert_that(response, matchers.has_status(200))
